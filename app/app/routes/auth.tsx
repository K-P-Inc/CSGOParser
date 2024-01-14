
// import './Auth.css';

import { Outlet, Navigate } from "react-router-dom";
import SigninForm from "~/components/forms/SigninForm";
// import SignupForm from "~/components/forms/SignupForm";

export default function Index() {

  return (
    <>
    <SigninForm />
    {/* <SignunForm /> */}
    </>
  )
}