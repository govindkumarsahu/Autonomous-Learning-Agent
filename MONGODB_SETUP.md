# MongoDB Setup Guide

## Issue: MongoDB Exit Code 100

This typically means MongoDB can't find or access its data directory.

## Quick Fix Options:

### Option 1: Start MongoDB with Custom Data Directory

1. Create a data directory:
```bash
mkdir C:\data\db
```

2. Start MongoDB with that directory:
```bash
mongod --dbpath C:\data\db
```

### Option 2: Use MongoDB Atlas (Cloud - Recommended for Quick Start)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a free cluster
4. Get your connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
5. Update `.env` file:
```
MONGODB_URL=mongodb+srv://your-username:your-password@your-cluster.mongodb.net/autonomous_learning_agent?retryWrites=true&w=majority
```

### Option 3: Install MongoDB as Windows Service

If MongoDB was installed as a service:
```bash
net start MongoDB
```

## Verify MongoDB is Running

Test connection:
```bash
mongosh
```

Or check if it's listening on port 27017:
```bash
netstat -an | findstr 27017
```

## For This Project (Fastest Option):

**Use MongoDB Atlas** - It's free, requires no local installation issues, and works immediately:

1. Sign up at mongodb.com/cloud/atlas
2. Create free cluster (takes 5 minutes)
3. Create database user
4. Whitelist your IP (or use 0.0.0.0/0 for development)
5. Get connection string
6. Update backend/.env with the connection string

The backend will automatically connect once MongoDB is accessible!
