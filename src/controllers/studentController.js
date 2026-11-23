const Student = require("../models/Student");

exports.getAll = async (req, res) => res.json(await Student.find());

exports.getOne = async (req, res) => {
  const s = await Student.findById(req.params.id).catch(() => null);
  if (!s) return res.status(404).json({ error: "Student not found" });
  res.json(s);
};

exports.create = async (req, res) => {
  try {
    res.status(201).json(await Student.create(req.body));
  } catch (e) {
    res.status(400).json({ error: e.message });
  }
};

exports.update = async (req, res) => {
  const s = await Student.findByIdAndUpdate(req.params.id, req.body, { new: true }).catch(() => null);
  if (!s) return res.status(404).json({ error: "Student not found" });
  res.json(s);
};

exports.remove = async (req, res) => {
  const s = await Student.findByIdAndDelete(req.params.id).catch(() => null);
  if (!s) return res.status(404).json({ error: "Student not found" });
  res.json({ message: "Student deleted" });
};
