import { Raid } from "./models";

export function groupBy<T>(
  array: Array<T>,
  prop: string
): { [key: string]: Array<T> } {
  return array.reduce(function(groups: { [key: string]: Array<T> }, item: any) {
    const val = item[prop];
    groups[val] = groups[val] || [];
    groups[val].push(item);
    return groups;
  }, {});
}

export const formatZone = (zone: Raid) => {
  switch (zone) {
    case Raid.BWL:
      return "Blackwing Lair";
    case Raid.MC:
      return "Molten Core";
    case Raid.ONY:
      return "Onyxia";
    case Raid.ZG:
      return "Zul'gurub";
    case Raid.NAXX:
      return "Naxx";
  }

  return zone;
};
