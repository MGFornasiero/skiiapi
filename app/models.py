from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

# =============================================================
# Custom Enum Types from DDL
# =============================================================

class GradeType(str, Enum):
    kyu = 'kyu'
    dan = 'dan'

class Sides(str, Enum):
    sx = 'sx'
    frontal = 'frontal'
    dx = 'dx'

class Movements(str, Enum):
    Fwd = 'Fwd'
    Still = 'Still'
    Bkw = 'Bkw'

class KataSeries(str, Enum):
    Heian = 'Heian'
    Tekki = 'Tekki'
    Sentei = 'Sentei'

class TargetHgt(str, Enum):
    Jodan = 'Jodan'
    Chudan = 'Chudan'
    Gedan = 'Gedan'

class WazaType(str, Enum):
    Uke = 'Uke'
    Uchi = 'Uchi'
    Geri = 'Geri'
    NA = 'NA'
    _ = '_'

class Tempo(str, Enum):
    Legato = 'Legato'
    Fast = 'Fast'
    Normal = 'Normal'
    Slow = 'Slow'
    Breath = 'Breath'

class Limbs(str, Enum):
    Mano = 'Mano'
    Braccio = 'Braccio'
    Piede = 'Piede'
    Gamba = 'Gamba'
    Ginochio = 'Ginochio'
    NA = 'NA'

class Hips(str, Enum):
    Hanmi = 'Hanmi'
    Shomen = 'Shomen'

class BeltColor(str, Enum):
    bianco = 'bianco'
    giallo = 'giallo'
    arancio = 'arancio'
    verde = 'verde'
    blu = 'blu'
    marrone = 'marrone'
    nero = 'nero'

class AbsoluteDirections(str, Enum):
    N = 'N'
    NE = 'NE'
    E = 'E'
    SE = 'SE'
    S = 'S'
    SO = 'SO'
    O = 'O'
    NO = 'NO'

# =============================================================
# Custom Composite Types from DDL
# =============================================================

class EmbusenPoints(BaseModel):
    x: int
    y: int

class BodyPart(BaseModel):
    limb: Limbs
    side: Sides

class DetailedNotes(BaseModel):
    arto: BodyPart
    description: Optional[str] = None
    explatation: Optional[str] = None
    note: Optional[str] = None

# =============================================================
# Domain Table Models (ski schema) and functions (public schema)
# =============================================================

# ski.targets -> public.get_targets(), public.get_target_info(), public.qry_ts_targets()
class Target(BaseModel):
    id_target: int
    name: str
    original_name: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    resource_url: Optional[str] = None

# ski.strikingparts -> public.get_strikingparts(), public.get_strikingparts_info(), public.qry_ts_strikingparts()
class StrikingPart(BaseModel):
    id_part: int
    name: str
    translation: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    resource_url: Optional[str] = None

# ski.technics -> public.get_technics(), public.get_technic_info(), public.qry_ts_technics()
class Technic(BaseModel):
    id_technic: int
    waza: Optional[WazaType] = None
    name: str
    description: Optional[str] = None
    notes: Optional[str] = None
    resource_url: Optional[str] = None

class TechnicDecomposition(BaseModel):
    id_decomposition: int
    technic_id: int
    component_order: int
    description: Optional[str] = None
    explatations: Optional[str] = None
    notes: Optional[str] = None
    resource_url: Optional[str] = None

# ski.stands -> public.get_stands(), public.get_stand_info(), public.qry_ts_stands()
class Stand(BaseModel):
    id_stand: int
    name: str
    description: Optional[str] = None
    illustration_url: Optional[str] = None
    notes: Optional[str] = None

# ski.grades -> public.get_grade()
class Grade(BaseModel):
    id_grade: int
    gtype: GradeType
    grade: int = Field(..., ge=1, le=10)
    color: Optional[BeltColor] = None

# ski.kihon_inventory -> public.get_kihons()
class KihonInventory(BaseModel):
    id_inventory: int
    grade_id: int
    number: int
    resources: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class KihonSequence(BaseModel):
    id_sequence: int
    inventory_id: int
    seq_num: int
    stand_id: int
    technic_id: int
    hips: Optional[Hips] = None
    gyaku: Optional[bool] = None
    target_hgt: Optional[TargetHgt] = None
    resources: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    resource_url: Optional[str] = None

class KihonTx(BaseModel):

    id_tx: int
    from_sequence: int
    to_sequence: int
    movement: Optional[Movements] = None
    resources: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    tempo: Optional[Tempo] = None
    resource_url: Optional[str] = None

class KihonStep(BaseModel): #get_kihon_steps()
    id_sequence: int
    inventory_id: int
    seq_num: int
    stand_id: int
    technic_id: int
    gyaku: bool | None
    target_hgt: TargetHgt | None
    notes: str | None
    resource_url: str | None
    stand_name: str | None
    technic_name: str | None

class KihonTx(BaseModel): #get_kihon_tx()
    id_tx: int
    from_sequence: int
    to_sequence: int
    movement: Movements | None
    tempo: Tempo | None
    notes: str | None
    resource_url: str | None

class KihonFormatted(BaseModel): #kihon_frmlist()
    number: int
    seq_num: int
    movement: Movements | None
    technic_id: int
    gyaku: bool | None
    tecnica: str | None
    stand_id: int
    posizione: str | None
    target_hgt: TargetHgt | None
    notes: str | None

# ski.kata_inventory -> public.show_katainventory(), public.get_katainfo()
class KataInventory(BaseModel):
    id_kata: int
    kata: str
    serie: Optional[KataSeries] = None
    starting_leg: Sides
    notes: Optional[str] = None
    resources: Optional[Dict[str, Any]] = None
    resource_url: Optional[str] = None

class KataSequence(BaseModel):
    id_sequence: int
    kata_id: int
    seq_num: int
    stand_id: int
    speed: Optional[Tempo] = None
    side: Optional[Sides] = None
    hips: Optional[Hips] = None
    embusen: Optional[EmbusenPoints] = None
    facing: Optional[AbsoluteDirections] = None
    kiai: Optional[bool] = None
    notes: Optional[str] = None
    remarks: Optional[List[DetailedNotes]] = None
    resources: Optional[Dict[str, Any]] = None
    resource_url: Optional[str] = None

class KataSequenceWaza(BaseModel):
    id_kswaza: int
    sequence_id: Optional[int] = None
    arto: Optional[BodyPart] = None
    technic_id: int
    strikingpart_id: Optional[int] = None
    technic_target_id: Optional[int] = None
    notes: Optional[str] = None
    resources: Optional[Dict[str, Any]] = None

class KataTx(BaseModel):
    id_tx: int
    from_sequence: int
    to_sequence: int
    tempo: Optional[Tempo] = None
    direction: Optional[Sides] = None
    intermediate_stand_id: Optional[int] = None
    notes: Optional[str] = None
    remarks: Optional[List[DetailedNotes]] = None
    resources: Optional[Dict[str, Any]] = None
    resource_url: Optional[str] = None

class KataTechnique(BaseModel): #json in tecniche di KataSequenceStep
    sequence_id: int
    arto: BodyPart
    technic_id: int
    Tecnica: str | None = Field(alias="tecnica")
    technic_target_id: int | None
    Obiettivo: str | None = Field(alias="obiettivo")
    waza_note: str | None
    waza_resources: dict | None

class KataSequenceStep(BaseModel): #get_katasequence()
    id_sequence: int
    kata_id: int
    seq_num: int
    stand_id: int
    posizione: str | None
    guardia: Sides | None
    facing: AbsoluteDirections | None
    Tecniche: List[KataTechnique] = Field(alias="tecniche")
    embusen: EmbusenPoints | None
    kiai: bool | None
    notes: str | None
    remarks: List[DetailedNotes] | None
    resources: dict | None
    resource_url: str | None

# ski.bunkai_inventory -> public.get_katabunkais()
class BunkaiInventory(BaseModel):
    id_bunkai: int
    kata_id: int
    version: Optional[int] = 1
    name: str
    description: Optional[str] = None
    notes: Optional[str] = None
    resources: Optional[Dict[str, Any]] = None
    resource_url: Optional[str] = None

class BunkaiSequence(BaseModel):
    id_bunkaisequence: int
    bunkai_id: int
    kata_sequence_id: int
    description: Optional[str] = None
    notes: Optional[str] = None
    remarks: Optional[List[DetailedNotes]] = None
    resources: Optional[Dict[str, Any]] = None
    resource_url: Optional[str] = None