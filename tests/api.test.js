const request = require("supertest");
const mongoose = require("mongoose");
const app = require("../src/app");

const MONGO_URI = process.env.MONGO_URI || "mongodb://localhost:27017/studentdb_test";

beforeAll(async () => {
  await mongoose.connect(MONGO_URI);
  await mongoose.connection.dropDatabase();
});

afterAll(async () => {
  await mongoose.connection.dropDatabase();
  await mongoose.disconnect();
});

describe("Student Management API", () => {
  let id;

  test("GET /health reports database connected", async () => {
    const res = await request(app).get("/health");
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ status: "ok", db: "connected" });
  });

  test("POST /api/students creates a student", async () => {
    const res = await request(app).post("/api/students").send({
      name: "Aarav Sharma", rollNo: "CS2026-001", email: "aarav@example.com", course: "B.Tech CSE", year: 2,
    });
    expect(res.status).toBe(201);
    expect(res.body.name).toBe("Aarav Sharma");
    id = res.body._id;
  });

  test("POST /api/students rejects missing fields", async () => {
    const res = await request(app).post("/api/students").send({ name: "No Roll" });
    expect(res.status).toBe(400);
  });

  test("GET /api/students lists students", async () => {
    const res = await request(app).get("/api/students");
    expect(res.status).toBe(200);
    expect(res.body).toHaveLength(1);
  });

  test("PUT /api/students/:id updates a student", async () => {
    const res = await request(app).put(`/api/students/${id}`).send({ year: 3 });
    expect(res.status).toBe(200);
    expect(res.body.year).toBe(3);
  });

  test("DELETE /api/students/:id deletes a student", async () => {
    const res = await request(app).delete(`/api/students/${id}`);
    expect(res.status).toBe(200);
    const after = await request(app).get(`/api/students/${id}`);
    expect(after.status).toBe(404);
  });
});
