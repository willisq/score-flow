export class Person{
    constructor({ firstname, lastname }){
        this.firstname = firstname;
        this.lastname = lastname;
    }

    toJSON(){
        return {
            firstname: this.firstname.value,
            lastname: this.lastname.value
        };
    }
}