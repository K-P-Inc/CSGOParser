
import * as React from "react"
import { useEffect, useRef } from "react"
import { DropdownMenuCheckboxItemProps } from "@radix-ui/react-dropdown-menu"
import { Check, ChevronDown, ChevronUp } from "lucide-react"
import { X } from "lucide-react"

import { Button } from "~/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "~/components/ui/dropdown-menu"

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select";

import { SubmitFunction } from "@remix-run/react"
import { Input } from "../ui/input"
import { WearType, StickersPattern, StickersType, WeaponType, ShopType } from "~/types"

type ShortNameMap<T extends string> = { [key in T]: string };

interface SelectorProps<T extends string> {
  items: T[];
  selectedItems: T[];
  setSelectedItems: React.Dispatch<React.SetStateAction<T[]>>;
  itemShortNames: ShortNameMap<T>;
  label: string;
}

export function GenericSelector<T extends string>({
  items,
  selectedItems,
  setSelectedItems,
  itemShortNames,
  label
}: SelectorProps<T>) {
  const [isOpen, setIsOpen] = React.useState(false);
  const [newSelectedItems, setNewSelectedItems] = React.useState<T[]>(selectedItems);

  return (
    <div className="flex">
      <DropdownMenu open={isOpen} onOpenChange={(open) => {
        if (open === true) {
          setNewSelectedItems(selectedItems);
        }
        setIsOpen(open);
      }}>
        <DropdownMenuTrigger asChild>
          <Button
            variant={isOpen || selectedItems.length ? "active" : "default"}
            size={selectedItems.length ? "left" : "default"}
          >
            {selectedItems.length === 0
              ? label
              : selectedItems.length === 1
              ? selectedItems[0]
              : `${itemShortNames[selectedItems[0]]} + ${selectedItems.length - 1} more`}
            {selectedItems.length === 0 && (
              <ChevronDown
                className="ml-2 h-4 w-4 opacity-50"
                onClick={(e: any) => {
                  e.stopPropagation();
                  alert("Please")
                }}
              />
            )}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuLabel>{label}</DropdownMenuLabel>
          <DropdownMenuSeparator className="mb-2"/>
          <div className="grid grid-cols-2 gap-2 mx-2 pt-2">
            {items.map((item, _) => (
              <DropdownMenuCheckboxItem
                key={item}
                checked={newSelectedItems.includes(item)}
                onSelect={(e: any) => {
                  e.preventDefault();
                  setNewSelectedItems((prevItems) =>
                    prevItems.includes(item)
                      ? prevItems.filter((i) => i !== item)
                      : [...prevItems, item]
                  )
                }}
              >
                {item}
              </DropdownMenuCheckboxItem>
            ))}
          </div>
          <div className="flex justify-end gap-4 mt-4">
            <Button variant="secondary" onClick={() => setNewSelectedItems([])}>Clear</Button>
            <Button variant="secondary" onClick={() => {
              setSelectedItems(newSelectedItems);
              setIsOpen(false);
            }}>Apply</Button>
          </div>
        </DropdownMenuContent>
      </DropdownMenu>
      {selectedItems.length > 0 &&
        <Button className="w-[30px]" size="right" onClick={(e: any) => { 
          e.preventDefault();
          setIsOpen(false);
          setSelectedItems([]);
        }}>
          <X className="h-4 w-4"/>
        </Button>
      }
    </div>
  );
}

function createItemsAndShortNames<T extends string>(items: T[]): { items: T[], itemShortNames: ShortNameMap<T> } {
  const itemShortNames = items.reduce((acc, item) => {
    acc[item] = item;
    return acc;
  }, {} as ShortNameMap<T>);

  return { items, itemShortNames };
}

// Usage example for WearType
export function WearSelector({
  selectedWears,
  setSelectedWears
}: {
  selectedWears: WearType[];
  setSelectedWears: React.Dispatch<React.SetStateAction<WearType[]>>;
}) {
  const wears: WearType[] = [
    "Factory New",
    "Minimal Wear",
    "Field-Tested",
    "Well-Worn",
    "Battle-Scarred"
  ];

  const wearsShort: ShortNameMap<WearType> = {
    "Factory New": "FN",
    "Minimal Wear": "MW",
    "Field-Tested": "FT",
    "Well-Worn": "WW",
    "Battle-Scarred": "BS"
  };

  return (
    <GenericSelector
      items={wears}
      selectedItems={selectedWears}
      setSelectedItems={setSelectedWears}
      itemShortNames={wearsShort}
      label="Wear"
    />
  );
}

// Usage example for WeaponType
export function WeaponSelector({
  selectedWeapons,
  setSelectedWeapons
}: {
  selectedWeapons: WeaponType[];
  setSelectedWeapons: React.Dispatch<React.SetStateAction<WeaponType[]>>;
}) {
  const { items: weapons, itemShortNames: weaponsShort } = createItemsAndShortNames([
    "AK-47", "M4A4", "M4A1-S", "AWP"
  ] as WeaponType[]);

  return (
    <GenericSelector
      items={weapons}
      selectedItems={selectedWeapons}
      setSelectedItems={setSelectedWeapons}
      itemShortNames={weaponsShort}
      label="Weapon"
    />
  );
}

export function ShopSelector({
  selectedShops,
  setSelectedShops
}: {
  selectedShops: ShopType[];
  setSelectedShops: React.Dispatch<React.SetStateAction<ShopType[]>>;
}) {
  const { items: shops, itemShortNames: ShortNames } = createItemsAndShortNames([
    "bitskins.com",
    "cs.money",
    "csfloat.com",
    "dmarket.com",
    "haloskins.com",
    "market.csgo.com",
    "skinbid.com",
    "skinport.com",
    "white.market",
    "skinbaron.de"
  ] as ShopType[]);

  return (
    <GenericSelector
      items={shops}
      selectedItems={selectedShops}
      setSelectedItems={setSelectedShops}
      itemShortNames={ShortNames}
      label="Market"
    />
  );
}

export function CategorySelector({
  selectedStickersPatterns,
  setSelectedStickersPatterns,
  selectedStickersTypes,
  setSelectedStickersTypes,
}: {
  selectedStickersPatterns: StickersPattern[],
  setSelectedStickersPatterns: React.Dispatch<React.SetStateAction<StickersPattern[]>>;
  selectedStickersTypes: StickersType[],
  setSelectedStickersTypes: React.Dispatch<React.SetStateAction<StickersType[]>>;
}) {
  const [isOpen, setIsOpen] = React.useState(false);
  const [newSelectedStickersPatterns, setNewSelectedStickersPatterns] = React.useState<StickersPattern[]>(selectedStickersPatterns);
  const [newSelectedSelectedStickersTypes, setNewSelectedStickersTypes] = React.useState<StickersType[]>(selectedStickersTypes);
  const stickersPatterns: StickersPattern[] = ["5-equal", "4-equal", "3-equal", "2-equal", "other"]
  const stickersTypes: StickersType[] = ["Gold", "Foil", "Holo", "Glitter"]
  const label = "Category"

  return (
    <div className="flex">
      <DropdownMenu open={isOpen} onOpenChange={(open) => {
        if (open === true) {
          setNewSelectedStickersPatterns(selectedStickersPatterns);
          setNewSelectedStickersTypes(selectedStickersTypes);
        }
        setIsOpen(open);
      }}>
        <DropdownMenuTrigger asChild>
          <Button
            variant={isOpen || selectedStickersPatterns.length || selectedStickersTypes.length ? "active" : "default"}
            size={selectedStickersPatterns.length || selectedStickersTypes.length ? "left" : "default"}
          >
            {selectedStickersPatterns.length === 0 && selectedStickersTypes.length === 0
              ? label
              : [selectedStickersPatterns, selectedStickersTypes]
                .filter(c => c.length > 0)
                .map(selectedItems => (
                  selectedItems.length === 1
                    ? selectedItems[0]
                    : `${selectedItems[0]} + ${selectedItems.length - 1} more`
                ))
                .join(", ")
            }
            {selectedStickersPatterns.length === 0 && selectedStickersTypes.length === 0 && (
              <ChevronDown
                className="ml-2 h-4 w-4 opacity-50"
                onClick={(e: any) => {
                  e.stopPropagation();
                  alert("Please")
                }}
              />
            )}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuLabel>Stickers' combo pattern</DropdownMenuLabel>
          <DropdownMenuSeparator className="mb-2"/>
          <div className="grid grid-cols-2 gap-2 mx-2 pt-2 mb-4">
            {stickersPatterns.map((item: StickersPattern, _) => (
              <DropdownMenuCheckboxItem
                key={item}
                checked={newSelectedStickersPatterns.includes(item)}
                onSelect={(e: any) => {
                  e.preventDefault();
                  setNewSelectedStickersPatterns((prevItems) =>
                    prevItems.includes(item)
                      ? prevItems.filter((i) => i !== item)
                      : [...prevItems, item]
                  )
                }}
              >
                {item}
              </DropdownMenuCheckboxItem>
            ))}
          </div>
          <DropdownMenuLabel>Sticker's type</DropdownMenuLabel>
          <DropdownMenuSeparator className="mb-2"/>
          <div className="grid grid-cols-2 gap-2 mx-2 pt-2">
            {stickersTypes.map((item: StickersType, _) => (
              <DropdownMenuCheckboxItem
                key={item}
                checked={newSelectedSelectedStickersTypes.includes(item)}
                onSelect={(e: any) => {
                  e.preventDefault();
                  setNewSelectedStickersTypes((prevItems) =>
                    prevItems.includes(item)
                      ? prevItems.filter((i) => i !== item)
                      : [...prevItems, item]
                  )
                }}
              >
                {item}
              </DropdownMenuCheckboxItem>
            ))}
          </div>
          <div className="flex justify-end gap-4 mt-4">
            <Button variant="secondary" onClick={() => {
                setSelectedStickersPatterns([]);
                setSelectedStickersTypes([]);
            }}>Clear</Button>
            <Button variant="secondary" onClick={() => {
              setSelectedStickersPatterns(newSelectedStickersPatterns);
              setSelectedStickersTypes(newSelectedSelectedStickersTypes);
              setIsOpen(false);
            }}>Apply</Button>
          </div>
        </DropdownMenuContent>
      </DropdownMenu>
      {(selectedStickersPatterns.length > 0 || selectedStickersTypes.length > 0) &&
        <Button className="w-[30px]" size="right" onClick={(e: any) => { 
          e.preventDefault();
          setIsOpen(false);
          setSelectedStickersPatterns([]);
          setSelectedStickersTypes([]);
        }}>
          <X className="h-4 w-4"/>
        </Button>
      }
    </div>
  );
}

interface MarketFilterParams {
  submit: SubmitFunction,
  wears: WearType[],
  weapons: WeaponType[],
  shops: ShopType[],
  stickersPatterns: StickersPattern[],
  stickersTypes: StickersType[],
  sort_by: string | undefined
}

export function MarketFilter({ wears, weapons, shops, stickersPatterns, stickersTypes, sort_by, submit } : MarketFilterParams) {
  const [selectedWears, setSelectedWears] = React.useState<WearType[]>(wears);
  const [selectedWeapons, setSelectedWeapons] = React.useState<WeaponType[]>(weapons);
  const [selectedShops, setSelectedShops] = React.useState<ShopType[]>(shops);
  const [selectedStickersPatterns, setSelectedStickersPatterns] = React.useState<StickersPattern[]>(stickersPatterns);
  const [selectedStickersTypes, setSelectedStickersTypes] = React.useState<StickersType[]>(stickersTypes);
  const [sortType, setSortType] = React.useState<string | undefined>(sort_by)

  useEffect(() => {
    if (
      wears !== selectedWears || weapons !== selectedWeapons || shops !== selectedShops || sort_by !== sortType ||
      selectedStickersPatterns != stickersPatterns || selectedStickersTypes != stickersTypes
    ) {
      const formData = new FormData(undefined);

      if (selectedWeapons.length > 0) {
        formData.set("weapon_types", selectedWeapons.join(","));
      }
      if (selectedWears.length > 0) {
        formData.set("wears", selectedWears.join(","));
      }
      if (selectedShops.length > 0) {
        formData.set("market_types", selectedShops.join(","));
      }
      if (selectedStickersPatterns.length > 0) {
        formData.set("stickers_patterns", selectedStickersPatterns.join(","));
      }
      if (selectedStickersTypes.length > 0) {
        formData.set("sticker_types", selectedStickersTypes.join(","));
      }
      if (sortType !== undefined) {
        formData.set("sort_by", sortType);
      }

      submit(formData);
    }
  }, [selectedWeapons, selectedWears, selectedShops, selectedStickersPatterns, selectedStickersTypes, sortType])

  return (
    <div className="w-full space-y-3">
      <div className="flex flex-wrap w-full flex-1 items-center gap-x-3 gap-y-3">
        <WeaponSelector selectedWeapons={selectedWeapons} setSelectedWeapons={setSelectedWeapons} />
        <WearSelector selectedWears={selectedWears} setSelectedWears={setSelectedWears} />
        <CategorySelector
          selectedStickersTypes={selectedStickersTypes} setSelectedStickersTypes={setSelectedStickersTypes}
          selectedStickersPatterns={selectedStickersPatterns} setSelectedStickersPatterns={setSelectedStickersPatterns}
        />
        <ShopSelector selectedShops={selectedShops} setSelectedShops={setSelectedShops} />
        <Select name="sort_by" value={sort_by} onValueChange={(value: string) => setSortType(value)}>
          <SelectTrigger className="w-[150px]">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Types</SelectLabel>
              <SelectItem value="newest">Newest</SelectItem>
              <SelectItem value="oldest">Oldest</SelectItem>
              <SelectItem value="profit_high_to_low">Highest Profit</SelectItem>
              <SelectItem value="profit_low_to_high">Lowest Profit</SelectItem>
              <SelectItem value="price_high_to_low">Highest Price</SelectItem>
              <SelectItem value="price_low_to_high">Lowest Price</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
    </div>
  )
}