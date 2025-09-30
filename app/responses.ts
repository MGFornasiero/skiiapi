// For /grade_inventory
export interface GradeInventory {
  gradi: string; // Note: This is a stringified dictionary
}

// For /kata_inventory
export interface KataInventory {
  kata: Record<string, number>;
}

// For /technic_inventory
export interface TechnicInfo {
  id_technic: number;
  waza: string;
  name: string;
  description: string | null;
  notes: string | null;
  resource_url: string | null;
}

export interface TechnicInventory {
  technics_inventory: Record<string, TechnicInfo>;
}

// For /stand_inventory
export interface StandInfo {
  id_stand: number;
  name: string;
  description: string | null;
  illustration_url: string | null;
  notes: string | null;
}

export interface StandInventory {
  stands_inventory: Record<string, StandInfo>;
}

// For /strikingparts_inventory
export interface StrikingPartInfo {
  id_part: number;
  name: string;
  translation: string | null;
  description: string | null;
  notes: string | null;
  resource_url: string | null;
}

export interface StrikingPartsInventory {
  strikingparts_inventory: Record<string, StrikingPartInfo>;
}

// For /target_inventory
export interface TargetInfo {
  id_target: number;
  name: string;
  original_name: string | null;
  description: string | null;
  notes: string | null;
  resource_url: string | null;
}

export interface TargetInventory {
  targets_inventory: Record<string, TargetInfo>;
}
export interface KihonStep {
  id_sequence: number;
  inventory_id: number;
  seq_num: number;
  stand: number;
  techinc: number; // Typo in original Python code
  gyaku: boolean;
  target_hgt: string;
  notes: string | null;
  resource_url: string | null;
  stand_name: string;
  technic_name: string;
}

export interface KihonTransaction {
  movement: string;
  tempo: string;
  notes: string | null;
  resource_url: string | null;
}

export interface KihonDetails {
  grade: string;
  grade_id: number;
  note: string | null;
  sequenza_n: number;
  tecniche: Record<string, KihonStep>;
  transactions: Record<string, KihonTransaction>;
  transactions_mapping_from: Record<string, number>;
  transactions_mapping_to: Record<string, number>;
}
export interface KataStep {
  id_sequence: number;
  kata_id: number;
  seq_num: number;
  stand_id: number;
  posizione: string;
  guardia: string;
  facing: number;
  tecniche: any; // Type could be more specific if the structure is known
  embusen: number;
  kiai: boolean;
  notes: string | null;
  remarks: any; // Type could be more specific if the structure is known
  resources: any; // Type could be more specific if the structure is known
  resource_url: string | null;
}

export interface KataTransaction {
  tempo: string;
  direction: string;
  note: string | null;
  remarks: any; // Type could be more specific if the structure is known
  resources: any; // Type could be more specific if the structure is known
  resource_url: string | null;
}

export interface KataDetails {
  kata_id: number;
  kata_name: string;
  serie: string;
  Gamba: string;
  notes: string | null;
  remarks: any; // Type could be more specific if the structure is known
  resources: any; // Type could be more specific if the structure is known
  resource_url: string | null;
  steps: Record<string, KataStep>;
  transactions: Record<string, KataTransaction>;
  transactions_mapping_from: Record<string, number>;
  transactions_mapping_to: Record<string, number>;
  bunkai_ids: number[];
}
export interface BunkaiInfo {
  kata_id: number;
  version: number;
  name: string;
  description: string | null;
  notes: string | null;
  resources: Record<string, any>; // Assuming a JSON object
  resource_url: string | null;
}

export interface BunkaiInventory {
  kata_id: number;
  bunkai_inventory: Record<string, BunkaiInfo>;
}

export interface BunkaiStep {
  id_bunkaisequence: number;
  bunkai_id: number;
  kata_sequence_id: number;
  description: string | null;
  notes: string | null;
  remarks: any; // JSON array from DB
  resources: any; // Type could be more specific
  resource_url: string | null;
}

export interface BunkaiDetails {
  bunkai_id: number;
  bunkai_steps: Record<string, BunkaiStep>;
}
export interface Relevance {
  abs_relevance: number;
  relative_relevance: number;
}

export interface FinderResult {
  ts: string;
  max_relevance: number;
  Targets_relevance: Record<string, Relevance>;
  Technics_relevance: Record<string, Relevance>;
  Stands_relevance: Record<string, Relevance>;
  Striking_parts_relevance: Record<string, Relevance>;
  Targets: Record<string, TargetInfo>;
  Technics: Record<string, TechnicInfo>;
  Stands: Record<string, StandInfo>;
  Striking_parts: Record<string, StrikingPartInfo>;
}

export interface KihonsApiResponse {
  grade: string;
  grade_id: number;
  kihons: KihonSequences;
}

export interface KihonSequences {
  [sequenzaNumber: string]: {
    [passaggioNumber: string]: KihonStepDetails;
  };
}

export interface KihonStepDetails {
  movement: string | null;
  technic_id: number;
  gyaku: boolean;
  tecnica: string;
  stand_id: number;
  Stand: string;
  Target: string;
  Note: string | null;
}
