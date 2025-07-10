import { api } from "@/service/AxiosBaseService";

export class ModalityService {
  static async findAll() {
    const { data } = await api.get("/modality/");

    return data;
  }
}
