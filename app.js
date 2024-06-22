const express = require('express');
const qr = require('qrcode');
const { createCanvas } = require('canvas');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve the index.html file for the root URL
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Handle form submission to generate QR code
app.post('/generate-qr', async (req, res) => {
  try {
    // Extract form data
    const { name, email, phone, membership } = req.body;

    // Create a QR code with user data
    const qrData = `${name}, ${email}, ${phone}, ${membership}`;
    const qrCodeBuffer = await generateQRCode(qrData);

    // Send the QR code as response
    res.set({ 'Content-Type': 'image/png' }).send(qrCodeBuffer);
  } catch (error) {
    console.error('Error generating QR code:', error);
    res.status(500).send('Error generating QR code');
  }
});

// Function to generate QR code from text
async function generateQRCode(text) {
  return new Promise((resolve, reject) => {
    qr.toBuffer(text, { errorCorrectionLevel: 'H' }, (err, buffer) => {
      if (err) reject(err);
      resolve(buffer);
    });
  });
}

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
