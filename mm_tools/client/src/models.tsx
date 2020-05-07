export enum Raid {
  MC = "MC",
  BWL = "BWL",
  ZG = "ZG",
  ONY = "ONY",
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
}
