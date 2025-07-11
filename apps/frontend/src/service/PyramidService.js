import { api } from "@/service/AxiosBaseService";

export class PyramidService {
  static championshipId = "25558000-df7a-49c2-a319-a11a94db4717";

  static async findPyramid() {
    const { data } = await api.get("/pyramid/", {
      params: {
        championshipId: PyramidService.championshipId,
      },
    });

    return data;
  }

  static async assemblePyramid(pyramidData) {
    await api.post("/pyramid/", {
      championship: PyramidService.championshipId,
      ...pyramidData,
    });
  }
}
