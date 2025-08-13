/**
 * Barebones Express server for Golden Knight Lounge frontend
 */
const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    environment: process.env.NODE_ENV || 'development',
    message: 'Golden Knight Lounge Frontend Server'
  });
});

// Root endpoint
app.get('/api', (req, res) => {
  res.json({
    message: 'Golden Knight Lounge Frontend API',
    version: '0.1.0'
  });
});

// Catch-all route for SPA (when we add React/Vue later)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Frontend server running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});