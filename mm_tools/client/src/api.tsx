import { Item, PriorityItem } from "./models";

interface ItemResult<T> {
  count: number;
  next?: string;
  previous?: string;
  results: Array<T>;
}

export class API {
  private apiRoot: string;
  constructor(apiRoot: string) {
    this.apiRoot = apiRoot;
  }

  getPriority = async () => {
    const result = await fetch(`${this.apiRoot}priorities/`, {
      redirect: "follow",
      mode: "cors",
      credentials: "include",
    });
    if (result.status !== 200) {
      throw new Error("Error getting priority");
    }
    return (await result.json()) as ItemResult<PriorityItem>;
  };

  updatePriority = async (itemIds: Array<number>) => {
    const result = await fetch(`${this.apiRoot}priorities/bulk_update/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: "follow",
      mode: "cors",
      credentials: "include",
      body: JSON.stringify({ items: itemIds }),
    });
    if (result.status == 400) {
      throw new Error((await result.json())["non_field_errors"]);
    }
    if (result.status !== 201) {
      throw new Error("generic error updating priority");
    }
  };

  searchItems = async (filter: string) => {
    const result = await fetch(`${this.apiRoot}items/?search=${filter}`, {
      redirect: "follow",
      mode: "cors",
      credentials: "include",
    });
    if (result.status !== 200) {
      throw new Error("Error getting items");
    }
    return (await result.json()) as ItemResult<Item>;
  };
}
