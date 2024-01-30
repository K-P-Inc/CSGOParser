import { SupabaseClient } from "@supabase/auth-helpers-remix";

export async function loadUser(supabase: SupabaseClient, userId: string): Promise<any> {
    let response = await supabase
        .from('users')
        .select('*')
        .eq('id', userId)
        .single()

    if (response.error) {
        throw new Error("Error updating user: " + response.error);
    }

    return response.data
}

export async function updateUser(supabase: SupabaseClient, userId: string, updateJSON: any): Promise<any> {
    let response = await supabase
        .from('users')
        .update(updateJSON)
        .eq('id', userId)
        .select()
        .single()

    if (response.error) {
        throw new Error("Error updating user: " + response.error);
    }

    return response.data
}