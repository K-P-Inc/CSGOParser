import { json, type LoaderFunctionArgs } from "@remix-run/node";
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { createSupabaseServerClient } from "~/supabase.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const response = new Response();

  const supabase = createSupabaseServerClient({ request, response });
  const { data, error } = await supabase
    .from('markets')
    .select('*')

  return json({});
}


export default function Index() {
  return (
    <div></div>
  );
}
