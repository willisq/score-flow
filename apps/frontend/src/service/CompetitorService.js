import { api } from "@/service/AxiosBaseService";

export class CompetitorService {
  championshipId = "25558000-df7a-49c2-a319-a11a94db4717";
  static async findByCategoryAndChampionShip(category) {
    const { data } = await api.get(
      "/competitor/by-category-and-championship/",
      {
        params: {
          category,
          championship: "25558000-df7a-49c2-a319-a11a94db4717",
        },
      }
    );

    return data;
  }

  static async findAll() {
    const { data } = await api.get("/competitor/");

    return data;
  }

  static async create(competitorData) {
    const { data } = await api.post("/competitor/", competitorData);

    return data;
  }
}
