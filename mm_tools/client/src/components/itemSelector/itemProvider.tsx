import { Item, Raid } from "../../models";
import { API } from "../../api";

export interface ItemProvider {
  getItems: (name: string) => Promise<Array<Item>>;
  abort: () => void;
}

export class APIItemProvider implements ItemProvider {
  private api: API;
  constructor(api: API) {
    this.api = api;
  }
  getItems = async (name: string): Promise<Item[]> => {
    const items = await this.api.searchItems(name);
    return items.results;
  };
  abort = () => {};
}
