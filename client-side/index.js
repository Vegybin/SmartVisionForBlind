import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import "dotenv/config";

const app = express();
const PORT = 3000;

// Resolve __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Serve static files from 'public' directory
app.use(express.static(path.join(__dirname, "public")));

app.get("/server-ip", (req, res) => {
    return res.send(process.env.SERVER_IP);
})

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
