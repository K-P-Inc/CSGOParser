
import * as React from "react"
import { useEffect, useRef, useState } from "react"
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
import { WearType, StickersPattern, StickersType, WeaponType, ShopType, CategoryType } from "~/types"
import { Switch } from "../ui/switch"

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
  const [isOpen, setIsOpen] = useState(false);
  const [newSelectedItems, setNewSelectedItems] = useState<T[]>(selectedItems);

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
                onClick={(e: any) => {}}
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

// Usage example for WearType
export function CategorySelector({
  selectedCategories,
  setSelectedCategories
}: {
  selectedCategories: CategoryType[];
  setSelectedCategories: React.Dispatch<React.SetStateAction<CategoryType[]>>;
}) {
  const { items: categories, itemShortNames: categoriesShort } = createItemsAndShortNames([
    "StatTrak™", "Normal"
  ] as CategoryType[]);


  return (
    <GenericSelector
      items={categories}
      selectedItems={selectedCategories}
      setSelectedItems={setSelectedCategories}
      itemShortNames={categoriesShort}
      label="Category"
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
    "skinbaron.de",
    "gamerpay.gg",
    "waxpeer.com"
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

export function StickersCategorySelector({
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
  const [isOpen, setIsOpen] = useState(false);
  const [newSelectedStickersPatterns, setNewSelectedStickersPatterns] = useState<StickersPattern[]>(selectedStickersPatterns);
  const [newSelectedSelectedStickersTypes, setNewSelectedStickersTypes] = useState<StickersType[]>(selectedStickersTypes);
  const stickersPatterns: StickersPattern[] = ["5-equal", "4-equal", "3-equal", "2-equal", "other"]
  const stickersTypes: StickersType[] = ["Gold", "Foil", "Holo", "Glitter"]
  const label = "Stickers";

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
                onClick={(e: any) => {}}
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


export function PriceSelector({
  selectedMinPrice,
  setSelectedMinPrice,
  selectedMaxPrice,
  setSelectedMaxPrice,
}: {
  selectedMinPrice: number | undefined,
  setSelectedMinPrice: React.Dispatch<React.SetStateAction<number | undefined>>;
  selectedMaxPrice: number | undefined,
  setSelectedMaxPrice: React.Dispatch<React.SetStateAction<number | undefined>>;
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [newSelectedMinPrice, setNewSelectedMinPrice] = useState<number | undefined>(selectedMinPrice);
  const [newSelectedMaxPrice, setNewSelectedMaxPrice] = useState<number | undefined>(selectedMaxPrice);
  const label = "Price";

  const handleMinPriceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseFloat(e.target.value);
    setNewSelectedMinPrice(value);
  };

  const handleMaxPriceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseFloat(e.target.value);
    setNewSelectedMaxPrice(value);
  };

  return (
    <div className="flex">
      <DropdownMenu open={isOpen} onOpenChange={(open) => {
        if (open) {
          setNewSelectedMinPrice(selectedMinPrice);
          setNewSelectedMaxPrice(selectedMaxPrice);
        }
        setIsOpen(open);
      }}>
        <DropdownMenuTrigger asChild>
          <Button
            variant={isOpen || selectedMinPrice !== undefined || selectedMaxPrice !== undefined ? "active" : "default"}
            size={selectedMinPrice !== undefined || selectedMaxPrice !== undefined ? "left" : "default"}
          >
            {(!selectedMinPrice && !selectedMaxPrice)
              ? label
              : `$ ${selectedMinPrice !== undefined ? selectedMinPrice.toFixed(2) : "0"} - $ ${selectedMaxPrice !== undefined ? selectedMaxPrice.toFixed(2) : "∞"}`
            }
            {(!selectedMinPrice && !selectedMaxPrice) && (
              <ChevronDown
                className="ml-2 h-4 w-4 opacity-50"
              />
            )}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuLabel>Price</DropdownMenuLabel>
          <DropdownMenuSeparator className="mb-2" />
          <div className="grid grid-cols-5 gap-2 mx-2 pt-2 mb-4 items-center">
            <div className="col-span-2">
              <small className="ml-1">From</small>
              <Input
                value={newSelectedMinPrice !== undefined ? newSelectedMinPrice : ''}
                onChange={handleMinPriceChange}
                className="w-[100px]"
                type="number"
                placeholder="$ 0.00"
              />
            </div>
            <div className="col-span-1 text-center mt-4">
              <span style={{ fontSize: "40px" }}>-</span>
            </div>
            <div className="col-span-2">
              <small className="ml-1">To</small>
              <Input
                value={newSelectedMaxPrice !== undefined ? newSelectedMaxPrice : ''}
                onChange={handleMaxPriceChange}
                className="w-[100px]"
                type="number"
                placeholder="$ ∞"
              />
            </div>
          </div>
          <div className="flex justify-end gap-4 mt-4">
            <Button variant="secondary" onClick={() => {
              setSelectedMaxPrice(undefined);
              setSelectedMinPrice(undefined);
            }}>Clear</Button>
            <Button variant="secondary" onClick={() => {
              setSelectedMaxPrice(newSelectedMaxPrice);
              setSelectedMinPrice(newSelectedMinPrice);
              setIsOpen(false);
            }}>Apply</Button>
          </div>
        </DropdownMenuContent>
      </DropdownMenu>
      {(selectedMinPrice !== undefined || selectedMaxPrice !== undefined) &&
        <Button className="w-[30px]" size="right" onClick={(e: any) => {
          e.preventDefault();
          setIsOpen(false);
          setSelectedMaxPrice(undefined);
          setSelectedMinPrice(undefined);
        }}>
          <X className="h-4 w-4" />
        </Button>
      }
    </div>
  );
}

export function SearchNameInput({ searchName, setSearchName } : { searchName: string, setSearchName: React.Dispatch<React.SetStateAction<string>> } ) {
  const [proxyValue, setProxyValue] = useState<string>(searchName);

  const handleChange = (e: any) => {
    setProxyValue(e.target.value);
  };

  // Function to handle blur event
  const handleBlur = (e: any) => {
    setSearchName(proxyValue);
  };

  // Function to handle key down event
  const handleKeyDown = (e: any) => {
    if (e.key === 'Enter') {
      setSearchName(proxyValue);
    }
  };

  useEffect(() => {
    const handler = setTimeout(() => {
      setSearchName(proxyValue);
    }, 1000);

    return () => {
      clearTimeout(handler);
    };
  }, [proxyValue]);

  return (
    <Input
      value={proxyValue}
      onChange={handleChange}
      onKeyDown={handleKeyDown}
      onBlur={handleBlur}
      className="w-[250px]" type="text" placeholder="Search name"
    />
  )
}

export function SortSelector(
  { sortBy, setSortBy } :
  { sortBy: string | undefined, setSortBy: React.Dispatch<React.SetStateAction<string | undefined>> }
) {
  return (
    <Select name="sort_by" value={sortBy} onValueChange={(value: string) => setSortBy(value)}>
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
  )
}

export function ProfitBasedSwitcher(
  { profitBased, setProfitBased } :
  { profitBased: string, setProfitBased: React.Dispatch<React.SetStateAction<string>> }
) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedNewProfitBased, setNewSelectedProfitBased] = useState<string>(profitBased);

  return (
    <div className="flex">
      <DropdownMenu open={isOpen} onOpenChange={(open) => {
        if (open) {
          setNewSelectedProfitBased(profitBased);
        }
        setIsOpen(open);
      }}>
        <DropdownMenuTrigger asChild>
          <Button
            variant={isOpen || profitBased !== 'steam' ? "active" : "default"}
            size={profitBased !== 'steam' ? "left" : "default"}
          >
            {(profitBased === 'steam')
              ? `Profit`
              : `Profit based on BUFF prices`
            }
            {(profitBased === 'steam') && (
              <ChevronDown
                className="ml-2 h-4 w-4 opacity-50"
              />
            )}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuLabel>Profit based on</DropdownMenuLabel>
          <DropdownMenuSeparator className="mb-2" />
          <div className="flex gap-2 mx-2 pt-2 mb-4 items-center justify-center">
            <small className="ml-1">Steam</small>
            <Switch
              checked={selectedNewProfitBased === "buff"}
              onCheckedChange={(checked) => setNewSelectedProfitBased(checked ? "buff" : "steam")}
              aria-readonly
            />
            <small className="ml-1">BUFF</small>
          </div>
          <div className="flex justify-end gap-4 mt-4">
            <Button variant="secondary" onClick={() => {
              setProfitBased('steam');
            }}>Clear</Button>
            <Button variant="secondary" onClick={() => {
              setProfitBased(selectedNewProfitBased);
              setIsOpen(false);
            }}>Apply</Button>
          </div>
        </DropdownMenuContent>
      </DropdownMenu>
      {(profitBased !== "steam") &&
        <Button className="w-[30px]" size="right" onClick={(e: any) => {
          e.preventDefault();
          setIsOpen(false);
          setProfitBased("steam");
        }}>
          <X className="h-4 w-4" />
        </Button>
      }
    </div>
  )
}

interface MarketFilterParams {
  submit: SubmitFunction,
  wears: WearType[],
  weapons: WeaponType[],
  shops: ShopType[],
  stickersPatterns: StickersPattern[],
  stickersTypes: StickersType[],
  categories: CategoryType[],
  search: string;
  profit_based: string;
  min_price: number | undefined;
  max_price: number | undefined;
  sort_by: string | undefined
}

export function MarketFilter(
  { wears, weapons, shops, stickersPatterns, stickersTypes, categories, search, min_price, max_price, sort_by, profit_based, submit } :
  MarketFilterParams
) {
  const [selectedWears, setSelectedWears] = useState<WearType[]>(wears);
  const [selectedWeapons, setSelectedWeapons] = useState<WeaponType[]>(weapons);
  const [selectedShops, setSelectedShops] = useState<ShopType[]>(shops);
  const [selectedStickersPatterns, setSelectedStickersPatterns] = useState<StickersPattern[]>(stickersPatterns);
  const [selectedStickersTypes, setSelectedStickersTypes] = useState<StickersType[]>(stickersTypes);
  const [selectedCategories, setSelectedCategories] = useState<CategoryType[]>(categories);
  const [selectedProfitBased, setSelectedProfitBased] = useState<string>(profit_based);
  const [selectedMinPrice, setSelectedMinPrice] = useState<number | undefined>(min_price);
  const [selectedMaxPrice, setSelectedMaxPrice] = useState<number | undefined>(max_price);
  const [searchName, setSearchName] = useState<string>(search);
  const [sortType, setSortType] = useState<string | undefined>(sort_by)

  useEffect(() => {
    if (
      wears !== selectedWears || weapons !== selectedWeapons || shops !== selectedShops || sort_by !== sortType ||
      selectedStickersPatterns != stickersPatterns || selectedStickersTypes != stickersTypes || searchName !== search ||
      categories !== selectedCategories || min_price !== selectedMinPrice || max_price !== selectedMaxPrice || selectedProfitBased !== profit_based
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
      if (searchName.length > 0) {
        formData.set("search", searchName);
      }
      if (selectedCategories.length > 0) {
        formData.set("categories", selectedCategories.join(","));
      }
      if (selectedMinPrice !== undefined) {
        formData.set("min_price", selectedMinPrice.toFixed(2));
      }
      if (selectedMaxPrice !== undefined) {
        formData.set("max_price", selectedMaxPrice.toFixed(2));
      }

      formData.set("profit_based", selectedProfitBased);

      submit(formData);
    }
  }, [
    selectedWeapons, selectedWears, selectedShops, selectedStickersPatterns, selectedStickersTypes,
    searchName, selectedCategories, sortType, selectedMinPrice, selectedMaxPrice, selectedProfitBased
  ])

  return (
    <div className="w-full space-y-3">
      <div className="flex flex-wrap w-full flex-1 items-center gap-x-3 gap-y-3">
        <PriceSelector
          selectedMinPrice={selectedMinPrice} setSelectedMinPrice={setSelectedMinPrice}
          selectedMaxPrice={selectedMaxPrice} setSelectedMaxPrice={setSelectedMaxPrice}
        />
        <WeaponSelector selectedWeapons={selectedWeapons} setSelectedWeapons={setSelectedWeapons} />
        <WearSelector selectedWears={selectedWears} setSelectedWears={setSelectedWears} />
        <StickersCategorySelector
          selectedStickersTypes={selectedStickersTypes} setSelectedStickersTypes={setSelectedStickersTypes}
          selectedStickersPatterns={selectedStickersPatterns} setSelectedStickersPatterns={setSelectedStickersPatterns}
        />
        <CategorySelector selectedCategories={selectedCategories} setSelectedCategories={setSelectedCategories}/>
        <ShopSelector selectedShops={selectedShops} setSelectedShops={setSelectedShops} />
        <ProfitBasedSwitcher profitBased={selectedProfitBased} setProfitBased={setSelectedProfitBased}/>
      </div>
      <div className="flex flex-wrap w-full flex-1 items-center gap-x-3 gap-y-3">
        <SearchNameInput searchName={searchName} setSearchName={setSearchName}/>
        <SortSelector sortBy={sortType} setSortBy={setSortType}/>
      </div>
    </div>
  )
}
