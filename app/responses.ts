import { 
    AbsoluteDirections, BodyPart, DetailedNotes, EmbusenPoints, Hips, KataSeries, Limbs, 
    Movements, Sides, TargetHgt, Tempo, WazaType 
} from "./type_admin_fe";

// For /grade_id/{gradetype}/{grade}
export interface GradeIdResponse {
  grade: number;
}

// For /numberofkihon/{grade_id}
export interface NumberOfKihonResponse {
  grade: number;
  n_kihon: number;
}

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

// For /kihon_list/{grade_id}/{sequenza}
export interface KihonStepInfo {
  id_sequence: number;
  inventory_id: number;
  seq_num: number;
  stand_id: number;
  technic_id: number;
  gyaku: boolean | null;
  target_hgt: TargetHgt | null;
  notes: string | null;
  resource_url: string | null;
  stand_name: string | null;
  technic_name: string | null;
}
export interface KihonTransaction {
  id_tx: number;
  from_sequence: number;
  to_sequence: number;
  movement: Movements | null;
  resources: Record<string, any> | Record<string, any>[] | null;
  notes: string | null;
  tempo: Tempo | null;
  resource_url: string | null;
}

export interface KihonListResponse {
  grade: string;
  grade_id: number;
  note: string | null;
  sequenza_n: number;
  tecniche: Record<string, KihonStepInfo>;
  transactions: Record<string, KihonTransaction>;
  transactions_mapping_from: Record<string, number>;
  transactions_mapping_to: Record<string, number>;
}

// For /kata/{kata_id}
export interface KataTechnique {
    sequence_id: number;
    arto: BodyPart | null;               // from models: arto can be nullable
    technic_id: number;
    tecnica: string | null;              // model attribute name is 'tecnica' (alias "Tecnica")
    strikingpart_id: number | null;
    strikingpart_name: string | null;
    technic_target_id: number | null;
    obiettivo: string | null;            // model attribute name is 'obiettivo' (alias "Obiettivo")
    waza_note: string | null;
    waza_resources: Record<string, any>[] | Record<string, any> | null; // allow single or multiple records
}

export interface KataSequenceStep {
  id_sequence: number;
  kata_id: number;
  seq_num: number;
  stand_id: number;
  posizione: string | null;
  speed: Tempo | null;
  guardia: Sides | null;
  hips: Hips | null;
  facing: AbsoluteDirections | null;
  Tecniche: KataTechnique[];           // model field name is 'Tecniche' (capital T)
  embusen: EmbusenPoints | null;
  kiai: boolean | null;                // can be null according to models
  notes: string | null;
  remarks: DetailedNotes[] | null;
  resources: Record<string, any> | Record<string, any>[] | null;
  resource_url: string | null;
}

export interface KataResponse {
  kata_id: number;
  kata_name: string;
  serie: KataSeries | null;
  Gamba: Sides;                         // starting_leg is a Sides enum in models
  notes: string | null;
  resources: Record<string, any> | Record<string, any>[] | null;
  resource_url: string | null;
  steps: Record<string, KataSequenceStep>;
  transactions: Record<string, KataTransaction>;
  transactions_mapping_from: Record<string, number>;
  transactions_mapping_to: Record<string, number>;
  bunkai_ids: Record<string, BunkaiSummary>;
}

export interface KataTransaction {
  id_tx: number;
  from_sequence: number;
  to_sequence: number;
  tempo: Tempo | null;
  direction: Sides | null;
  intermediate_stand_id: number | null;
  notes: string | null;
  remarks: DetailedNotes[] | null;
  resources: Record<string, any> | Record<string, any>[] | null;
  resource_url: string | null;
}

export interface BunkaiSummary {
  version: number;
  name: string;
  description: string | null;
  notes: string | null;
  resources: Record<string, any> | Record<string, any>[] | null; // This is from BunkaiInventory model
  resource_url: string | null;
}
// For /bunkai_inventory/{kata_id}
export interface BunkaiInfo {
  id_bunkai: number;
  kata_id: number;
  version: number;
  name: string;
  description: string | null;
  notes: string | null;
  resources: Record<string, any> | Record<string, any>[] | null;
  resource_url: string | null;
}

export interface BunkaiStep {
  id_bunkaisequence: number;
  bunkai_id: number;
  kata_sequence_id: number;
  description: string | null;
  notes: string | null;
  remarks: DetailedNotes[] | null;
  resources: Record<string, any> | Record<string, any>[] | null;
  resource_url: string | null;
}

// For /finder
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

// For /info_technic/{item_id}
export interface InfoTechnicResponse {
    id: number;
    info_technic: TechnicInfo | {
        id_technic: null;
        waza: null;
        name: null;
        description: null;
        notes: null;
        resource_url: null;
    };
}

// For /technics_decomposition/{item_id}
export interface TechnicDecompositionStep {
    step_num: number;
    stand_id: number;
    technic_id: number;
    gyaku: boolean;
    target_hgt: TargetHgt;
    notes: string | null;
    resource_url: string | null;
}

export interface TechnicDecompositionResponse {
    id: number;
    technic_decomposition: Record<string, TechnicDecompositionStep> | [];
}

// For /info_stand/{item_id}
export interface InfoStandResponse {
    id: number;
    info_stand: StandInfo | {
        id_stand: null;
        name: null;
        description: null;
        illustration_url: null;
        notes: null;
    };
}

// For /info_strikingparts/{item_id}
export interface InfoStrikingPartsResponse {
    id: number;
    info_strikingparts: StrikingPartInfo | {
        id_part: null;
        name: null;
        translation: null;
        description: null;
        notes: null;
        resource_url: null;
    };
}

// For /kihons/{grade_id}
export interface KihonsResponse {
  grade: string;
  grade_id: number;
  kihons: KihonSequences;
}

export interface KihonSequences {
  [number: string]: {
    [seq_num: string]: KihonFormattedDetails;
  };
}

export interface KihonFormattedDetails {
  movement: Movements | null;
  technic_id: number;
  gyaku: boolean | null;
  tecnica: string | null;
  stand_id: number;
  Stand: string | null;
  Target: TargetHgt | null;
  Note: string | null;
}

// For /utils/present_kata/{kata_id}
export interface PresentKataResponse {
    info: Record<string, KataSequenceStep>;
}

// For /secure/
export interface SecureDataResponse {
    data: string;
}
