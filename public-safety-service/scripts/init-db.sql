-- Initialize Swakopmund Municipality Public Safety Service Database
-- This script sets up the initial database configuration

-- Set timezone
SET timezone = 'Africa/Windhoek';

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create indexes for better performance (will be created by SQLAlchemy migrations)
-- These are additional optimizations

-- Log the initialization
DO $$
BEGIN
    RAISE NOTICE 'Swakopmund Municipality Public Safety Service database initialized successfully';
END
$$; 