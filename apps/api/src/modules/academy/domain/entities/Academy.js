import { Name } from "#academy/domain/valueObjects/Name.js";

export class Academy {
  constructor({ id, name, instructor }) {
    this.id = id;
    this.name = name;
    this.instructor = instructor;
  }

  changeName(newName) {
    this.name = new Name(newName);
  }

  changeInstructor(newInstructorId) {
    this.instructor = newInstructorId;
  }

  toJSON() {
    return {
      id: this.id,
      name: this.name.value,
      instructor: this.instructor,
    };
  }
}
