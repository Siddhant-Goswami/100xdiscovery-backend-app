-- Enable UUID extension if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Add email column to existing profiles table if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'profiles' 
                  AND column_name = 'email') THEN
        ALTER TABLE profiles ADD COLUMN email TEXT;
        ALTER TABLE profiles ADD COLUMN user_id uuid REFERENCES auth.users(id);
    END IF;
END $$;

-- Create profiles table with auth user reference
CREATE TABLE IF NOT EXISTS profiles (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id uuid REFERENCES auth.users(id),
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    skills TEXT[] NOT NULL,
    bio TEXT NOT NULL,
    projects TEXT[] NOT NULL,
    collaboration_interests TEXT[] NOT NULL,
    portfolio_url TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
        REFERENCES auth.users(id)
        ON DELETE CASCADE
);

-- Create index on email and user_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_profiles_email ON profiles(email);
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DO $$ 
BEGIN
    DROP POLICY IF EXISTS "Profiles are viewable by everyone" ON profiles;
    DROP POLICY IF EXISTS "Users can create their own profile" ON profiles;
    DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
    DROP POLICY IF EXISTS "Users can delete own profile" ON profiles;
EXCEPTION
    WHEN undefined_object THEN
        NULL;
END $$;

-- Create RLS Policies

-- Allow users to view all profiles
CREATE POLICY "Profiles are viewable by everyone" 
    ON profiles FOR SELECT 
    USING (true);

-- Allow authenticated users to insert their own profile
CREATE POLICY "Users can create their own profile" 
    ON profiles FOR INSERT 
    WITH CHECK (
        auth.uid() = user_id AND 
        email = auth.email()
    );

-- Allow users to update their own profile
CREATE POLICY "Users can update own profile" 
    ON profiles FOR UPDATE 
    USING (auth.uid() = user_id);

-- Allow users to delete their own profile
CREATE POLICY "Users can delete own profile" 
    ON profiles FOR DELETE 
    USING (auth.uid() = user_id);

-- Function to automatically set user_id and email on insert
CREATE OR REPLACE FUNCTION public.handle_new_profile()
RETURNS TRIGGER AS $$
BEGIN
    NEW.user_id := auth.uid();
    NEW.email := auth.email();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Drop existing trigger if exists
DROP TRIGGER IF EXISTS on_profile_created ON profiles;

-- Create trigger
CREATE TRIGGER on_profile_created
    BEFORE INSERT ON profiles
    FOR EACH ROW
    EXECUTE FUNCTION handle_new_profile(); 