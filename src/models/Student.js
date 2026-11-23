const mongoose = require("mongoose");

const studentSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },
    rollNo: { type: String, required: true, unique: true },
    email: { type: String, required: true },
    course: { type: String, required: true },
    year: { type: Number, min: 1, max: 5 },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Student", studentSchema);
