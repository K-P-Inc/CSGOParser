import { Link } from "@remix-run/react";

export default function WorkProgress() {
  return (
    <section className="flex flex-1">
      <div className="flex flex-col items-center justify-center w-full bg-dark-1 text-white p-4">
        <div className="text-center">
          <h1 className="text-6xl text-primary-500 font-bold mb-4">Work in Progress</h1>
          <p className="text-xl text-white mb-8">This page is currently under construction</p>
          <div className="mt-6">
          <Link to="/" className="text-xl font-medium text-primaryGreen">
            Go back home
            <span aria-hidden="true"> &rarr;</span>
          </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
