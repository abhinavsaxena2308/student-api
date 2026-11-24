const path = require("path");
const express = require("express");
const mongoose = require("mongoose");
const studentRoutes = require("./routes/studentRoutes");

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

app.get("/api", (req, res) => res.json({ message: "Student Management API is running" }));
app.get("/health", (req, res) =>
  res.json({ status: "ok", db: mongoose.connection.readyState === 1 ? "connected" : "disconnected" })
);
app.use("/api/students", studentRoutes);

module.exports = app;
