-- table to store information about processed files from s3
create table if not exists public.processed_files
(
    id serial primary key,
    s3_key text not null,
    s3_bucket text not null,
    s3_etag text not null,
    processed_at timestamp with time zone default now(),
    status text default 'done',
    updated_at timestamp with time zone default now(),
    UNIQUE (s3_key, s3_etag)
);