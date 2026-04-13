// --- Base Entities ---

export interface Sex {
  id: string;
  name: string;
}

export interface Rank {
  id: string;
  name: string;
  classification: number;
  isBlackBelt: boolean;
}

export interface Person {
  id: string;
  firstName: string;
  lastName: string;
}

export interface Academy {
  id: string;
  name: string;
  instructor: Person;
}

export interface Competitor {
  id: string;
  firstName: string;
  lastName: string;
  academy: Academy;
  rank: Rank;
  sex: Sex;
  weight: number | null;
  height: number | null;
  age: number | null;
  specialCondition: boolean;
}

// --- Create DTOs ---

export interface SexCreate {
  name: string;
}

export interface RankCreate {
  name: string;
  classification: number;
  isBlackBelt: boolean;
}

export interface PersonCreate {
  firstName: string;
  lastName: string;
}

export interface AcademyCreate {
  name: string;
  instructor: PersonCreate;
}

export interface CompetitorCreate {
  firstName: string;
  lastName: string;
  academyId: string;
  rankId: string;
  sexId: string;
  weight?: number | null;
  height?: number | null;
  age?: number | null;
  specialCondition?: boolean;
}

export interface CompetitorBulkCreate {
  competitors: CompetitorCreate[];
}

export interface CompetitorFilters {
  name?: string;
  academyId?: string;
  rankId?: string;
  sexId?: string;
  specialCondition?: boolean;
}
