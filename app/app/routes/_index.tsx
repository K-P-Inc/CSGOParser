import { json, type LoaderFunctionArgs } from "@remix-run/node";
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { createSupabaseServerClient } from "~/supabase.server";
import { FullLogoIcon } from "~/assets/images";


export default function Index() {
  return (
    <div className="flex flex-1">
      <div className="home-container">
        <img src={FullLogoIcon}/>
      </div>
    </div>
  );
}
