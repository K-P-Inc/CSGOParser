import { useEffect, useState } from "react";
import { useActionData, useOutletContext, useSubmit } from "@remix-run/react";
import { OutletContext } from "~/types";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "~/components/ui/form";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { useToast } from "~/components/ui/use-toast";
import { ProfileValidation, ProfileSchema } from "~/lib/validation";
import { Form as FormRemix } from "@remix-run/react";
import { zodResolver } from "@hookform/resolvers/zod";
import { FieldErrors } from "react-hook-form";
import { getMarketCSGOBalance, testMarketCSGOToken } from "~/models/market.csgo.api";
import { updateUser, loadUser } from "~/models/supabase.api";
import { getSteamUserData } from "~/models/steam.api";
import { AccountIcon } from "~/assets/images";
import { ActionFunctionArgs, json } from "@remix-run/node";
import { createSupabaseServerClient } from "~/supabase.server";
import { useRemixForm, getValidatedFormData, } from "remix-hook-form";

export const action = async ({ request } : ActionFunctionArgs) => { 
  const response = new Response();

  const supabase = createSupabaseServerClient({ request, response });
  const { data: { session } } = await supabase.auth.getSession();
  const userData = await loadUser(supabase, session?.user.id || "");

  const {
    errors,
    data,
    receivedValues: defaultValues
  }  = await getValidatedFormData<ProfileSchema>(request, zodResolver(ProfileValidation))

  if (errors) {
    return json({ errors, defaultValues });
  }

  let updaterJson = undefined;
  let needsUpdate = false;
  let iserror = false

  try {
    if (userData.market_csgo_api_key !== data.market_csgo_api_key) {
      await testMarketCSGOToken(data.market_csgo_api_key as string);
      const response = await getMarketCSGOBalance(data.market_csgo_api_key as string)

      const currenyConverter = {
        "USD": response.money as number,
        "RUB": response.money / 90.0 as number,
        "EUR": response.money * 0.9 as number,
      }

      if (!updaterJson) {
        updaterJson = {}
      }

      updaterJson = {
        ...updaterJson,
        market_csgo_api_key: data.market_csgo_api_key,
        market_csgo_balance: currenyConverter[response.currency as ("USD" | "RUB" | "EUR")]
      };
      needsUpdate = true;
    }
  } catch (error) {
    console.log(error);
    iserror = true
  }

  try {
    if (userData.steam_id !== data.steam_id || userData.steam_api_key !== data.steam_api_key) {
      const response = await getSteamUserData(data.steam_api_key as string, data.steam_id.toString())

      if (!updaterJson) {
        updaterJson = {}
      }

      updaterJson = { ...updaterJson, steam_id: data.steam_id, steam_api_key: data.steam_api_key, ...response };
      needsUpdate = true;
    }
  } catch (error) {
    console.log(error);
    iserror = true
  }

  if (!iserror && updaterJson !== undefined) {
    updateUser(supabase, userData?.id, updaterJson);
  }

  return json({ updaterJson })
}

export default function Index() {
  const { userData, setUserData } = useOutletContext<OutletContext>();
  const { toast } = useToast()
  const [isUpdating, setIsUpdating] = useState(false);

  const form = useRemixForm<ProfileSchema>({
    resolver: zodResolver(ProfileValidation),
    submitHandlers: {
      onValid: () => {
        toast({ title: 'Success', description: 'Data updated' })
      },
      onInvalid: () => {
        toast({ title: 'Error', description: 'form.formState.errors' })
      }
    },
    defaultValues: {
      ...userData
    }
  })

  return (
    <div className="profile-container">
      <div className="profile-inner_container">
        <div className="flex xl:flex-row flex-col max-xl:items-center flex-1 gap-7">
          <img
            src={
              userData?.icon_url || AccountIcon
            }
            alt="profile"
            className="w-28 h-28 lg:h-36 lg:w-36 rounded-full"
          />
          <div className="flex flex-col flex-1 justify-between md:mt-2">
            <div className="flex flex-col w-full">
              <h1 className="text-center xl:text-left h3-bold md:h1-semibold w-full">
                {userData?.steam_name || "Steam name"}
              </h1>
              <p className="small-regular md:body-medium text-light-3 text-center xl:text-left">
                ${userData && userData.market_csgo_balance ? userData?.market_csgo_balance.toFixed(2) : '$$$'}
              </p>
            </div>
          </div>
        </div>
      </div>
      <div className="flex h-screen flex-1 items-center flex-col">
        <Form {...form}>
          <div className="w-[350px] flex-center flex-col">
            <FormRemix
              method="post"
              className="flex flex-col gap-5 w-full mt-4 rounded-2xl border border-dark-4 bg-dark-2 p-8"
            >
              <FormField
                control={form.control}
                name="steam_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="shad-form_label">Steam ID</FormLabel>
                    <FormControl>
                      <Input type="bigint" className="shad-input" {...field} max="999999999999999999"/>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="steam_api_key"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="shad-form_label">Steam API Key</FormLabel>
                    <FormControl>
                      <Input type="password" className="shad-input" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <div className="rounded border border-primary-500 px-4 my-2" />
              <FormField
                control={form.control}
                name="market_csgo_api_key"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="shad-form_label">Market CS:GO API Key</FormLabel>
                    <FormControl>
                      <Input type="password" className="shad-input" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <div className="rounded border border-primary-500 px-4 my-2" />

              <Button type="submit" className={!isUpdating ? "shad-button_primary" : "shad-button_ghost "} disabled={isUpdating}>
                Update profile
              </Button>
            </FormRemix >
          </div>
        </Form>
      </div>
      <pre>{JSON.stringify(form.formState.errors, null, 2)}</pre>
    </div>
  );
};
