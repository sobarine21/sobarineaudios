const express = require('express');
const multer = require('multer');
const fs = require('fs');
const pdfParse = require('pdf-parse');
const googleTTS = require('google-tts-api');
const path = require('path');

// Create an instance of the Express application
const app = express();
const port = 3000;

// Setup for file uploads
const upload = multer({ dest: 'uploads/' });

// Serve static files (e.g., audio files)
app.use(express.static('public'));

// Home route for uploading PDF
app.get('/', (req, res) => {
  res.send(`
    <h1>Podcast Creator</h1>
    <form action="/upload" method="POST" enctype="multipart/form-data">
      <label>Upload content PDF:</label><br>
      <input type="file" name="pdfFile" accept="application/pdf" required/><br><br>
      <button type="submit">Upload PDF</button>
    </form>
  `);
});

// Route for uploading PDF and generating podcast
app.post('/upload', upload.single('pdfFile'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send("No file uploaded.");
  }

  try {
    // Read and extract text from the uploaded PDF
    const pdfData = fs.readFileSync(req.file.path);
    const pdfText = await pdfParse(pdfData);
    const text = pdfText.text.trim();

    if (!text) {
      return res.status(400).send("No text found in the PDF.");
    }

    // Generate audio from the extracted text
    const audioUrl = await googleTTS.getAudioUrl(text, {
      lang: 'en',
      slow: false,
      host: 'https://translate.google.com',
    });

    // Save the audio file to the 'public' directory
    const audioFileName = `podcast_${Date.now()}.mp3`;
    const audioFilePath = path.join(__dirname, 'public', audioFileName);

    // Download the audio file using Node.js 'request' or similar method
    const download = require('node-fetch');
    const response = await download(audioUrl);
    const buffer = await response.buffer();
    fs.writeFileSync(audioFilePath, buffer);

    // Send the response back with a link to download the audio
    res.send(`
      <h2>Podcast Audio Generated!</h2>
      <p>Click the link below to download your podcast:</p>
      <a href="/${audioFileName}" download>Download Podcast Audio</a>
      <br><br>
      <audio controls>
        <source src="/${audioFileName}" type="audio/mpeg">
        Your browser does not support the audio element.
      </audio>
    `);
  } catch (error) {
    console.error("Error generating podcast:", error);
    res.status(500).send("Error generating podcast.");
  } finally {
    // Clean up uploaded PDF file
    fs.unlinkSync(req.file.path);
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Podcast Creator app running at http://localhost:${port}`);
});
