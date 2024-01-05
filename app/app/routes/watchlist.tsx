import React from 'react';
import { Switch } from '~/components/ui/switch';
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "~/components/ui/table"

const WeaponCategory = ({ title, weapons }) => {
  return (
    <Table>
      <TableHead><h2 className="h3-bold md:h2-bold text-left w-full">{title}</h2></TableHead>
      <TableBody>
        {weapons.map((weapon, index) => (
          <TableRow key={index}>
            <TableCell className="font-medium">{weapon}</TableCell>
            <TableCell><Switch id={`airplane-mode-${index}`} /></TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

const WatchList = () => {
  const weaponCategories = [
    { title: 'Pistols', weapons: ['CZ75-Auto', 'Desert Eagle', 'Dual Berettas', 'Five-Seven', 'Glock-18', 'P2000', 'P250', 'R8 Revolver', 'Tec-9', 'USP-S'] },
    { title: 'Assault Rifles', weapons: ['AK-47', 'AUG', 'FAMAS', 'Galil AR', 'M4A1-S', 'M4A4', 'SG 553'] },
    { title: 'SMGs', weapons: ['MAC-10', 'MP5-SD', 'MP7', 'MP9', 'P90', 'PP-Bizon', 'UMP-45'] },
    { title: 'Sniper Rifles', weapons: ['AWP', 'G3SG1', 'SCAR-20', 'SSG 08'] },
    { title: 'Shot Guns', weapons: ['MAG-7', 'Nova', 'Sawed-Off', 'XM1014'] },
    { title: 'Machine Guns', weapons: ['M249', 'Negev'] },
  ];

  return (
    <div style={{
      flexDirection: 'column',
      display: 'flex',
      justifyContent: 'center'
    }}>
      <Table className="tables-container">
        {weaponCategories.map((category, index) => (
          <TableCell key={index}>
            <WeaponCategory title={category.title} weapons={category.weapons} />
          </TableCell>
        ))}
      </Table>
    </div>
  );
};

export default WatchList;
