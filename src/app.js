const express = require("express");
const mongoose = require("mongoose");
const studentRoutes = require("./routes/studentRoutes");

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI || "mongodb://localhost:27017/studentdb";

app.get("/", (req, res) => res.json({ message: "Student Management API is running" }));
app.get("/health", (req, res) =>
  res.json({ status: "ok", db: mongoose.connection.readyState === 1 ? "connected" : "disconnected" })
);
app.use("/api/students", studentRoutes);

mongoose
  .connect(MONGO_URI)
  .then(() => console.log("Connected to MongoDB at", MONGO_URI))
  .catch((err) => console.error("MongoDB connection error:", err.message));

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`));
