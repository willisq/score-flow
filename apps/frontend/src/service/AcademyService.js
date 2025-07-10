import { api } from "@/service/AxiosBaseService";

export class AcademyService {
	static async createAcademy(academyData) {
		const { data } = await api.post(
			"/academy/",
			academyData,
		);

		return data;
	}

	static async getAllAcademies(){
		const { data } = await api.get("/academy/");

		return data;
	}
}
