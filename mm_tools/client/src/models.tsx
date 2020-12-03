export enum Raid {
  MC = "MC",
  BWL = "BWL",
  AQ_40 = "AQ40",
  ZG = "ZG",
  ONY = "ONY",
  NAXX = "NAXX"
}

export interface PriorityItem {
  id: number;
  added: string;
  updated: string;
  item: Item;
}

export interface Item {
  id: number;
  zone: Raid;
  name: string;
  type: string;
  slot: string;
  tiers: Array<ItemTier>;
}

export interface ItemTier {
  id: number;
  name: string;
  color: string;
}