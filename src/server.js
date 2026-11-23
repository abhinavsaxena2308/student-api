const mongoose = require("mongoose");
const app = require("./app");

const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI || "mongodb://localhost:27017/studentdb";

mongoose
  .connect(MONGO_URI)
  .then(() => console.log("Connected to MongoDB at", MONGO_URI))
  .catch((err) => console.error("MongoDB connection error:", err.message));

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`));
