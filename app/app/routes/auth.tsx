import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "~/components/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { SigninValidation } from "~/lib/validation";
import { Button } from "~/components/ui/button";
import { Input } from "~/components/ui/input";
import { useForm } from "react-hook-form";
import { redirect, useOutletContext } from "@remix-run/react";
import type { OutletContext } from "~/types";
import * as z from "zod";
import { useToast } from "~/components/ui/use-toast";

export default function Index() {
  const { supabase } = useOutletContext<OutletContext>();
  const { toast } = useToast()
  const form = useForm<z.infer<typeof SigninValidation>>({
    resolver: zodResolver(SigninValidation),
    defaultValues: {
      email: "",
      password: "",
    }
  });

  const handleSignup = async (user: z.infer<typeof SigninValidation>) => {
    const { data: response } = await supabase.auth.signInWithPassword({
      email: user.email,
      password: user.password
    })

    if (!response.user) {
      toast({ title: "Wrong credentials" });
    } else {
      toast({ title: "Success login!" });
      form.reset();
      redirect("/");
    }
  }

  return (
    <main className="flex h-screen flex-1 justify-center items-center flex-col">
      <Form {...form}>
        <div className="sm:w-420 flex-center flex-col">

          <h2 className="h3-bold md:h2-bold pt-5 sm:pt-12">
            Log in to your account
          </h2>

          <p className="text-light-3 small-medium md:base-regular mt-2">
            Welcome back! Please enter your details.
          </p>

          <form
            onSubmit={form.handleSubmit(handleSignup)}
            className="flex flex-col gap-5 w-full mt-4">
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="shad-form_label">Email</FormLabel>
                  <FormControl>
                    <Input type="text" className="shad-input" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="shad-form_label">Password</FormLabel>
                  <FormControl>
                    <Input type="password" className="shad-input" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button type="submit" className="shad-button_primary">
              Log in
            </Button>
          </form>
        </div>
      </Form>
    </main>
  )
}