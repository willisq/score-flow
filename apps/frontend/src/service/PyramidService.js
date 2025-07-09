import { api } from "@/service/AxiosBaseService";

export class PyramidService{
    static async findPyramid(){
        const { data } = await api.get("/pyramid/", {
            params: {
                championshipId: "25558000-df7a-49c2-a319-a11a94db4717",
                age: 7,
                sexes: ["b1529907-996b-43a5-9d20-9505618017d8"],
                ranks: ["662b5ad0-a16d-404e-9aa8-3f6a37f1a981"]
            }
        });

        return data;
        
    }
}