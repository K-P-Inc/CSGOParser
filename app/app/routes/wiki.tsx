import React, { useState, useEffect } from 'react';
import { DownOutlined, UpOutlined } from '@ant-design/icons';
import { useNavigate } from "@remix-run/react";

import {
  collection_overpass,
  collection_gallary,
  collection_graphic_design,
  collection_sport_field,
  collection_the_revolution,
  collection_anubis,
  collection_kilowatt,
  collection_limited_1,
  collection_recoil,
  collection_dreams_nightmares,
  collection_train_2021,
  collection_dust_2_2021,
  collection_mirage_2021,
  collection_snakebite,
  collection_operation_riptide,
  collection_vertigo_2021,
  collection_havoc,
  collection_ancient,
  collection_control,
  collection_operation_broken_fang,
  collection_st_marc,
  collection_canals,
  collection_prisma_2,
  collection_fracture,
  collection_x_ray,
  collection_cs20,
  collection_shattered_web,
  collection_norse,
  collection_prisma,
  collection_clutch,
  collection_blacksite,
  collection_danger_zone,
  collection_2018_nuke_collection,
  collection_2018_inferno_collection,
  collection_horizon_collection,
  collection_spectrum_2_collection,
  collection_operation_hydra_collection,
  collection_spectrum_collection,
  collection_glove_collection,
  collection_gamma_2_collection,
  collection_gamma_collection,
  collection_chroma_3_collection,
  collection_wildfire_collection,
  collection_revolver_case_collection,
  collection_shadow_collection,
  collection_rising_sun_collection,
  collection_gods_and_monsters_collection,
  collection_chop_shop_collection,
  collection_falchion_collection,
  collection_chroma_2_collection,
  collection_chroma_collection,
  collection_vanguard_collection,
  collection_cache_collection,
  collection_esports_2014_summer_collection,
  collection_breakout_collection,
  collection_baggage_collection,
  collection_overpass_collection,
  collection_cobblestone_collection,
  collection_bank_collection,
  collection_huntsman_collection,
  collection_phoenix_collection,
  collection_arms_deal_3_collection,
  collection_esports_2013_winter_collection,
  collection_winter_offensive_collection,
  collection_italy_collection,
  collection_mirage_collection,
  collection_safehouse_collection,
  collection_dust_2_collection,
  collection_lake_collection,
  collection_train_collection,
  collection_arms_deal_2_collection,
  collection_alpha_collection,
  collection_bravo_collection,
  collection_assault_collection,
  collection_dust_collection,
  collection_office_collection,
  collection_nuke_collection,
  collection_aztec_collection,
  collection_inferno_collection,
  collection_arms_deal_collection,
  collection_militia_collection,
  collection_vertigo_collection,
  collection_esports_2013_collection } from "~/assets/images";

const sticker_collection = [
  {
    id: 1,
    title: "Paris 2023 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_paris2023_group_legends.png",
    date: "May 21, 2023",
    redirect: "",
  },
  {
    id: 2,
    title: "Paris 2023 Legends Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_paris2023_legends.png",
    date: "May 21, 2023",
    redirect: "",
  },
  {
    id: 3,
    title: "Paris 2023 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_paris2023_group_challengers.png",
    date: "May 21, 2023",
    redirect: "",
  },
  {
    id: 4,
    title: "Paris 2023 Challengers Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_paris2023_challengers.png",
    date: "May 21, 2023",
    redirect: "",
  },
  {
    id: 5,
    title: "Paris 2023 Contenders Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_paris2023_contenders.png",
    date: "May 21, 2023",
    redirect: "/capsules/paris-2023-contenders-sticker-capsule",
  },
  {
    id: 6,
    title: "Paris 2023 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_paris2023_group_champions.png",
    date: "May 21, 2023",
    redirect: "",
  },
  {
    id: 7,
    title: "Paris 2023 Contenders Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_paris2023_group_contenders.png",
    date: "May 21, 2023",
    redirect: "",

  },
  {
    id: 8,
    title: "Espionage Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_community2022_capsule.png",
    date: "December 15, 2022",
    redirect: "",
  },
  {
    id: 9,
    title: "Rio 2022 Contenders Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_group_contenders.png",
    date: "October 21, 2022",
    redirect: "",
  },
  {
    id: 10,
    title: "Rio 2022 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_group_challengers.png",
    date: "October 21, 2022",
    redirect: "",
  },
  {
    id: 11,
    title: "Rio 2022 Legends Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_legends.png",
    date: "October 21, 2022",
    redirect: "",
  },
  {
    id: 12,
    title: "Katowice 2019 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2019_legends.png",
    date: "February 20, 2019",
    redirect: "",
  },
  {
    id: 13,
    title: "Katowice 2019 Minor Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2019_contenders.png",
    date: "February 20, 2019",
    redirect: "",
  },
  {
    id: 14,
    title: "Autograph Capsule | Fnatic",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/columbus2016_fntc.png",
    date: "March 29, 2016",
    redirect: "",
  },
  {
    id: 15,
    title: "Autograph Capsule | Cloud9",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/columbus2016_c9.png",
    date: "March 29, 2016",
    redirect: "",
  },
  {
    id: 16,
    title: "Autograph Capsule | Astralis",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/columbus2016_astr.png",
    date: "March 29, 2016",
    redirect: "",
  },
  {
    id: 17,
    title: "Autograph Capsule | mousesports",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2016_mss.png",
    date: "July 5, 2016",
    redirect: "",
  },
  {
    id: 18,
    title: "Autograph Capsule | Flipsid3 Tactics",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2016_flip.png",
    date: "July 5, 2016",
    redirect: "",
  },
  {
    id: 19,
    title: "Autograph Capsule | G2 Esports",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2016_g2.png",
    date: "July 5, 2016",
    redirect: "",
  },
  {
    id: 20,
    title: "Rio 2022 Contenders Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_group_contenders.png",
    date: "October 21, 2022",
    redirect: ""
  },
  {
    id: 21,
    title: "Rio 2022 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_group_challengers.png",
    date: "October 21, 2022",
    redirect: ""
  },
  {
    id: 22,
    title: "Rio 2022 Legends Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_legends.png",
    date: "October 21, 2022",
    redirect: ""
  },
  {
    id: 23,
    title: "Rio 2022 Challengers Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_challengers.png",
    date: "October 21, 2022",
    redirect: ""
  },
  {
    id: 24,
    title: "Rio 2022 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_group_champions.png",
    date: "October 21, 2022",
    redirect: ""
  },
  {
    id: 25,
    title: "Rio 2022 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_group_legends.png",
    date: "October 21, 2022",
    redirect: ""
  },
  {
    id: 26,
    title: "Berlin 2019 Minor Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_berlin2019_contenders.png",
    date: "August 23, 2019",
    redirect: ""
  },
  {
    id: 27,
    title: "Autograph Capsule | Cloud9 | MLG Columbus 2016",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/columbus2016_c9.png",
    date: "March 29, 2016",
    redirect: ""
  },
  {
    id: 28,
    title: "Autograph Capsule | Astralis | MLG Columbus 2016",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/columbus2016_astr.png",
    date: "March 29, 2016",
    redirect: ""
  },
  {
    id: 29,
    title: "Katowice 2019 Minor Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2019_contenders.png",
    date: "February 13, 2019",
    redirect: ""
  },
  {
    id: 30,
    title: "Autograph Capsule | mousesports | Cologne 2016",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2016_mss.png",
    date: "July 5, 2016",
    redirect: ""
  },
  {
    id: 31,
    title: "London 2018 Minor Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_london2018_group_contenders.png",
    date: "September 5, 2018",
    redirect: ""
  },
  {
    id: 32,
    title: "Autograph Capsule | Flipsid3 Tactics | Cologne 2016",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2016_flip.png",
    date: "July 5, 2016",
    redirect: ""
  },
  {
    id: 33,
    title: "Autograph Capsule | G2 Esports | Cologne 2016",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2016_g2.png",
    date: "July 5, 2016",
    redirect: ""
  },
  {
    id: 34,
    title: "Autograph Capsule | FaZe Clan | Atlanta 2017",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/atlanta2017_faze.png",
    date: "January 22, 2017",
    redirect: ""
  },
  {
    id: 35,
    title: "Autograph Capsule | Team Dignitas | Cologne 2016",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2016_dig.png",
    date: "July 5, 2016",
    redirect: ""
  },
  {
    id: 36,
    title: "Katowice 2019 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2019_legends.png",
    date: "February 20, 2019",
    redirect: ""
  },
  {
    id: 37,
    title: "Katowice 2019 Minor Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2019_contenders.png",
    date: "February 20, 2019",
    redirect: ""
  },
  {
    id: 38,
    title: "Autograph Capsule | Fnatic | MLG Columbus 2016",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/columbus2016_fntc.png",
    date: "March 29, 2016",
    redirect: ""
  },
  {
    id: 39,
    title: "London 2018 Returning Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_london2018_challengers.png",
    date: "September 5, 2018",
    redirect: ""
  },
  {
    id: 40,
    title: "London 2018 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_london2018_legends.png",
    date: "September 5, 2018",
    redirect: ""
  },
  {
    id: 41,
    title: "Berlin 2019 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_berlin2019_legends.png",
    date: "August 23, 2019",
    redirect: ""
  },
  {
    id: 42,
    title: "Berlin 2019 Returning Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_berlin2019_challengers.png",
    date: "August 23, 2019",
    redirect: ""
  },
  {
    id: 43,
    title: "Katowice 2019 Returning Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2019_challengers.png",
    date: "February 20, 2019",
    redirect: ""
  },
  {
    id: 44,
    title: "London 2018 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_london2018_champions.png",
    date: "September 5, 2018",
    redirect: ""
  },
  {
    id: 45,
    title: "Boston 2018 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_boston2018_legends.png",
    date: "January 19, 2018",
    redirect: ""
  },
  {
    id: 46,
    title: "Boston 2018 Returning Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_boston2018_challengers.png",
    date: "January 19, 2018",
    redirect: ""
  },
  {
    id: 47,
    title: "Atlanta 2017 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/atlanta2017_legends.png",
    date: "January 22, 2017",
    redirect: ""
  },
  {
    id: 48,
    title: "Atlanta 2017 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/atlanta2017_challengers.png",
    date: "January 22, 2017",
    redirect: ""
  },
  {
    id: 49,
    title: "Atlanta 2017 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/atlanta2017_champions.png",
    date: "January 22, 2017",
    redirect: ""
  },
  {
    id: 50,
    title: "Cologne 2016 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2016_challengers.png",
    date: "July 5, 2016",
    redirect: ""
  },
  {
    id: 51,
    title: "Cologne 2016 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2016_legends.png",
    date: "July 5, 2016",
    redirect: ""
  },
  {
    id: 52,
    title: "MLG Columbus 2016 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/columbus2016_challengers.png",
    date: "March 29, 2016",
    redirect: ""
  },
  {
    id: 53,
    title: "MLG Columbus 2016 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/columbus2016_legends.png",
    date: "March 29, 2016",
    redirect: ""
  },
  {
    id: 54,
    title: "Cluj-Napoca 2015 Challengers (Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cluj2015_challengers.png",
    date: "October 28, 2015",
    redirect: ""
  },
  {
    id: 55,
    title: "Cluj-Napoca 2015 Legends (Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cluj2015_legends.png",
    date: "October 28, 2015",
    redirect: ""
  },
  {
    id: 56,
    title: "Cologne 2015 Challengers (Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2015_challengers.png",
    date: "August 20, 2015",
    redirect: ""
  },
  {
    id: 57,
    title: "Cologne 2015 Legends (Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2015_legends.png",
    date: "August 20, 2015",
    redirect: ""
  },
  {
    id: 58,
    title: "Katowice 2015 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2015_challengers.png",
    date: "February 26, 2015",
    redirect: ""
  },
  {
    id: 59,
    title: "Katowice 2015 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2015_legends.png",
    date: "February 26, 2015",
    redirect: ""
  },
  {
    id: 60,
    title: "DreamHack 2014 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/dhw2014_legends.png",
    date: "November 26, 2014",
    redirect: ""
  },
  {
    id: 61,
    title: "DreamHack 2014 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/dhw2014_challengers.png",
    date: "November 26, 2014",
    redirect: ""
  },
  {
    id: 62,
    title: "Cologne 2014 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2014_challengers.png",
    date: "August 14, 2014",
    redirect: ""
  },
  {
    id: 63,
    title: "Cologne 2014 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/cologne2014_legends.png",
    date: "August 14, 2014",
    redirect: ""
  },
  {
    id: 64,
    title: "Katowice 2014 Challengers",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2014_challengers.png",
    date: "March 5, 2014",
    redirect: ""
  },
  {
    id: 65,
    title: "Katowice 2014 Legends",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2014_legends.png",
    date: "March 5, 2014",
    redirect: ""
  },
  {
    id: 66,
    title: "Community Sticker Capsule 1",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_community01.png",
    date: "February 5, 2014",
    redirect: ""
  },
  {
    id: 67,
    title: "Sticker Capsule 2",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_02.png",
    date: "December 18, 2013",
    redirect: ""
  },
  {
    id: 68,
    title: "Sticker Capsule 1",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_01.png",
    date: "August 8, 2013",
    redirect: ""
  },
  {
    id: 69,
    title: "Perfect World Sticker Capsule 1",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_perfectworld01.png",
    date: "May 18, 2017",
    redirect: ""
  },
  {
    id: 70,
    title: "Perfect World Sticker Capsule 2",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_perfectworld02.png",
    date: "July 19, 2017",
    redirect: ""
  },
  {
    id: 71,
    title: "Sugarface Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_sugarface_capsule.png",
    date: "October 22, 2020",
    redirect: ""
  },
  {
    id: 72,
    title: "Recoil Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_recoil_capsule.png",
    date: "July 1, 2022",
    redirect: ""
  },
  {
    id: 73,
    title: "Revolution Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_revolution_capsule.png",
    date: "February 10, 2023",
    redirect: ""
  },
  {
    id: 74,
    title: "Skill Groups Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_skillgroups_capsule.png",
    date: "August 31, 2022",
    redirect: ""
  },
  {
    id: 75,
    title: "Antwerp 2022 Contenders Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_contenders.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 76,
    title: "Antwerp 2022 Challengers Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_challengers.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 77,
    title: "Antwerp 2022 Legends Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_legends.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 78,
    title: "Antwerp 2022 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_champions_signatures.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 79,
    title: "Stockholm 2021 Contenders Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_contenders.png",
    date: "October 26, 2021",
    redirect: ""
  },
  {
    id: 80,
    title: "Stockholm 2021 Legends Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_legends.png",
    date: "October 26, 2021",
    redirect: ""
  },
  {
    id: 81,
    title: "Stockholm 2021 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_champions_signatures.png",
    date: "October 26, 2021",
    redirect: ""
  },
  {
    id: 82,
    title: "Stockholm 2021 Challengers Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_challengers.png",
    date: "October 26, 2021",
    redirect: ""
  },
  {
    id: 83,
    title: "Rmr 2020 Legends",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rmr2020_legends.png",
    date: "April 22, 2020",
    redirect: ""
  },
  {
    id: 84,
    title: "Rmr 2020 Challengers",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rmr2020_challengers.png",
    date: "April 22, 2020",
    redirect: ""
  },
  {
    id: 85,
    title: "Rmr 2020 Contenders",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rmr2020_contenders.png",
    date: "April 22, 2020",
    redirect: ""
  },
  {
    id: 86,
    title: "Berlin 2019 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_berlin2019_champions_autograph.png",
    date: "September 5, 2019",
    redirect: ""
  },
  {
    id: 87,
    title: "Berlin 2019 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_berlin2019_legends_autograph.png",
    date: "August 23, 2019",
    redirect: ""
  },
  {
    id: 88,
    title: "Berlin 2019 Returning Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_berlin2019_challengers_autograph.png",
    date: "August 23, 2019",
    redirect: ""
  },
  {
    id: 89,
    title: "Berlin 2019 Minor Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_berlin2019_minors_autograph.png",
    date: "August 23, 2019",
    redirect: ""
  },
  {
    id: 90,
    title: "Katowice 2019 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2019_champions_autograph.png",
    date: "March 3, 2019",
    redirect: ""
  },
  {
    id: 91,
    title: "Katowice 2019 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2019_legends_autograph.png",
    date: "February 20, 2019",
    redirect: ""
  },
  {
    id: 92,
    title: "Katowice 2019 Returning Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2019_challengers_autograph.png",
    date: "February 20, 2019",
    redirect: ""
  },
  {
    id: 93,
    title: "London 2018 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_london2018_champions_autograph.png",
    date: "September 23, 2018",
    redirect: ""
  },
  {
    id: 94,
    title: "London 2018 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_london2018_legends_autograph.png",
    date: "September 5, 2018",
    redirect: ""
  },
  {
    id: 95,
    title: "London 2018 Returning Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_london2018_challengers_autograph.png",
    date: "September 5, 2018",
    redirect: ""
  },
  {
    id: 96,
    title: "Boston 2018 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_boston2018_champions_autograph.png",
    date: "January 28, 2018",
    redirect: ""
  },
  {
    id: 97,
    title: "Boston 2018 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_boston2018_legends_autograph.png",
    date: "January 19, 2018",
    redirect: ""
  },
  {
    id: 98,
    title: "Boston 2018 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_boston2018_challengers_autograph.png",
    date: "January 19, 2018",
    redirect: ""
  },
  {
    id: 99,
    title: "Krakow 2017 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_krakow2017_champions_autograph.png",
    date: "July 23, 2017",
    redirect: ""
  },
  {
    id: 100,
    title: "Krakow 2017 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_krakow2017_legends_autograph.png",
    date: "July 16, 2017",
    redirect: ""
  },
  {
    id: 101,
    title: "Krakow 2017 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_krakow2017_challengers_autograph.png",
    date: "July 16, 2017",
    redirect: ""
  },
  {
    id: 102,
    title: "Atlanta 2017 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_atlanta2017_champions_autograph.png",
    date: "January 29, 2017",
    redirect: ""
  },
  {
    id: 103,
    title: "Atlanta 2017 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_atlanta2017_legends_autograph.png",
    date: "January 22, 2017",
    redirect: ""
  },
  {
    id: 104,
    title: "Atlanta 2017 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_atlanta2017_challengers_autograph.png",
    date: "January 22, 2017",
    redirect: ""
  },
  {
    id: 105,
    title: "Cologne 2016 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2016_champions_autograph.png",
    date: "July 10, 2016",
    redirect: ""
  },
  {
    id: 106,
    title: "Cologne 2016 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2016_legends_autograph.png",
    date: "July 5, 2016",
    redirect: ""
  },
  {
    id: 107,
    title: "Cologne 2016 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2016_challengers_autograph.png",
    date: "July 5, 2016",
    redirect: ""
  },
  {
    id: 108,
    title: "MLG Columbus 2016 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_mlg2016_champions_autograph.png",
    date: "April 3, 2016",
    redirect: ""
  },
  {
    id: 109,
    title: "MLG Columbus 2016 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_mlg2016_legends_autograph.png",
    date: "March 29, 2016",
    redirect: ""
  },
  {
    id: 110,
    title: "MLG Columbus 2016 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_mlg2016_challengers_autograph.png",
    date: "March 29, 2016",
    redirect: ""
  },
  {
    id: 111,
    title: "Cluj-Napoca 2015 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cluj2015_champions_autograph.png",
    date: "November 1, 2015",
    redirect: ""
  },
  {
    id: 112,
    title: "Cluj-Napoca 2015 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cluj2015_legends_autograph.png",
    date: "October 28, 2015",
    redirect: ""
  },
  {
    id: 113,
    title: "Cluj-Napoca 2015 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cluj2015_challengers_autograph.png",
    date: "October 28, 2015",
    redirect: ""
  },
  {
    id: 114,
    title: "Cologne 2015 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2015_champions_autograph.png",
    date: "August 23, 2015",
    redirect: ""
  },
  {
    id: 115,
    title: "Cologne 2015 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2015_legends_autograph.png",
    date: "August 20, 2015",
    redirect: ""
  },
  {
    id: 116,
    title: "Cologne 2015 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2015_challengers_autograph.png",
    date: "August 20, 2015",
    redirect: ""
  },
  {
    id: 117,
    title: "Katowice 2015 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2015_champions_autograph.png",
    date: "March 1, 2015",
    redirect: ""
  },
  {
    id: 118,
    title: "Katowice 2015 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2015_legends_autograph.png",
    date: "February 26, 2015",
    redirect: ""
  },
  {
    id: 119,
    title: "Katowice 2015 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2015_challengers_autograph.png",
    date: "February 26, 2015",
    redirect: ""
  },
  {
    id: 120,
    title: "DreamHack 2014 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_dhw2014_champions_autograph.png",
    date: "November 30, 2014",
    redirect: ""
  },
  {
    id: 121,
    title: "DreamHack 2014 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_dhw2014_legends_autograph.png",
    date: "November 26, 2014",
    redirect: ""
  },
  {
    id: 122,
    title: "DreamHack 2014 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_dhw2014_challengers_autograph.png",
    date: "November 26, 2014",
    redirect: ""
  },
  {
    id: 123,
    title: "Cologne 2014 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2014_champions_autograph.png",
    date: "August 17, 2014",
    redirect: ""
  },
  {
    id: 124,
    title: "Cologne 2014 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2014_legends_autograph.png",
    date: "August 14, 2014",
    redirect: ""
  },
  {
    id: 125,
    title: "Cologne 2014 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2014_challengers_autograph.png",
    date: "August 14, 2014",
    redirect: ""
  },
  {
    id: 126,
    title: "Community Sticker Capsule 2",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_community02.png",
    date: "July 1, 2014",
    redirect: ""
  },
  {
    id: 127,
    title: "Team Roles Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_teamroles_capsule.png",
    date: "September 7, 2022",
    redirect: ""
  },
  {
    id: 128,
    title: "Antwerp 2022 Contenders Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_contenders_autograph.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 129,
    title: "Antwerp 2022 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_challengers_autograph.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 130,
    title: "Antwerp 2022 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_legends_autograph.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 131,
    title: "Stockholm 2021 Contenders Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_contenders_autograph.png",
    date: "October 26, 2021",
    redirect: ""
  },
  {
    id: 132,
    title: "Stockholm 2021 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_challengers_autograph.png",
    date: "October 26, 2021",
    redirect: ""
  },
  {
    id: 133,
    title: "Stockholm 2021 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_legends_autograph.png",
    date: "October 26, 2021",
    redirect: ""
  },
  {
    id: 134,
    title: "Operation Broken Fang Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_broken_fang_capsule.png",
    date: "December 3, 2020",
    redirect: ""
  },
  {
    id: 135,
    title: "CS:GO Sticker Capsule 2",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_csgo2_capsule.png",
    date: "February 10, 2014",
    redirect: ""
  },
  {
    id: 136,
    title: "CS:GO Sticker Capsule 1",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_csgo1_capsule.png",
    date: "February 7, 2014",
    redirect: ""
  },
  {
    id: 137,
    title: "Bestiary Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_bestiary_capsule.png",
    date: "March 27, 2020",
    redirect: ""
  },
  {
    id: 138,
    title: "Halo Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_halo_capsule.png",
    date: "December 19, 2019",
    redirect: ""
  },
  {
    id: 139,
    title: "Shattered Web Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_shattered_web_capsule.png",
    date: "November 18, 2019",
    redirect: ""
  },
  {
    id: 140,
    title: "CS20 Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cs20_capsule.png",
    date: "October 18, 2019",
    redirect: ""
  },
  {
    id: 141,
    title: "Skill Groups Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_skillgroups_capsule.png",
    date: "August 31, 2022",
    redirect: ""
  },
  {
    id: 142,
    title: "Legends Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_legends_capsule.png",
    date: "July 1, 2019",
    redirect: ""
  },
  {
    id: 143,
    title: "Loyalty Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_loyalty_capsule.png",
    date: "December 6, 2018",
    redirect: ""
  },
  {
    id: 144,
    title: "Pinups Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_pinups_capsule.png",
    date: "February 13, 2015",
    redirect: ""
  },
  {
    id: 145,
    title: "Slid3 Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_slid3_capsule.png",
    date: "October 10, 2019",
    redirect: ""
  },
  {
    id: 146,
    title: "Unicorn Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_unicorn_capsule.png",
    date: "March 15, 2017",
    redirect: ""
  },
  {
    id: 147,
    title: "Enfu Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_enfu_capsule.png",
    date: "June 4, 2015",
    redirect: ""
  },
  {
    id: 148,
    title: "Sugarface Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_sugarface_capsule.png",
    date: "October 22, 2020",
    redirect: ""
  },
  {
    id: 149,
    title: "Perfect World Sticker Capsule 1",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_perfectworld01.png",
    date: "May 18, 2017",
    redirect: ""
  },
  {
    id: 150,
    title: "Perfect World Sticker Capsule 2",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_perfectworld02.png",
    date: "July 19, 2017",
    redirect: ""
  },
  {
    id: 151,
    title: "Community Sticker Capsule 1",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_community01.png",
    date: "February 5, 2014",
    redirect: ""
  },
  {
    id: 152,
    title: "Sticker Capsule 2",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_02.png",
    date: "December 18, 2013",
    redirect: ""
  },
  {
    id: 153,
    title: "Sticker Capsule 1",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_01.png",
    date: "August 8, 2013",
    redirect: ""
  },
  {
    id: 154,
    title: "Krakow 2017 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_krakow2017_legends.png",
    date: "July 16, 2017",
    redirect: ""
  },
  {
    id: 155,
    title: "Krakow 2017 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_krakow2017_challengers.png",
    date: "July 16, 2017",
    redirect: ""
  },
  {
    id: 156,
    title: "Krakow 2017 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_krakow2017_champions.png",
    date: "July 23, 2017",
    redirect: ""
  },
  {
    id: 157,
    title: "Community Graffiti Box 1",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_community_graffiti_01.png",
    date: "October 6, 2016",
    redirect: ""
  },
  {
    id: 158,
    title: "Graffiti Box",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_valve_graffiti_01.png",
    date: "October 6, 2016",
    redirect: ""
  },
  {
    id: 159,
    title: "Half-Life: Alyx Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_hlalyx.png",
    date: "March 23, 2020",
    redirect: ""
  },
  {
    id: 160,
    title: "Feral Predators Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_feral_predators.png",
    date: "August 6, 2021",
    redirect: ""
  },
  {
    id: 161,
    title: "Poorly Drawn Sticker Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_poorly_drawn.png",
    date: "May 3, 2021",
    redirect: ""
  },
  {
    id: 162,
    title: "Antwerp 2022 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_champions.png",
    date: "May 21, 2022",
    redirect: ""
  },
  {
    id: 163,
    title: "Antwerp 2022 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_legends.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 164,
    title: "Antwerp 2022 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_challengers.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 165,
    title: "Antwerp 2022 Contenders (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_contenders.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 166,
    title: "Stockholm 2021 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_champions.png",
    date: "November 7, 2021",
    redirect: ""
  },
  {
    id: 167,
    title: "Stockholm 2021 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_legends.png",
    date: "October 26, 2021",
    redirect: ""
  },
  {
    id: 168,
    title: "Stockholm 2021 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_challengers.png",
    date: "October 26, 2021",
    redirect: ""
  },
  {
    id: 169,
    title: "Stockholm 2021 Contenders (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_contenders.png",
    date: "October 26, 2021",
    redirect: ""
  },
  {
    id: 170,
    title: "Operation Broken Fang Patches",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_patch_pack_broken_fang.png",
    date: "December 3, 2020",
    redirect: ""
  },
  {
    id: 171,
    title: "Shattered Web Agents",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_character_pack_shattered_web.png",
    date: "November 18, 2019",
    redirect: ""
  },
  {
    id: 172,
    title: "Shattered Web Patches",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_patch_pack_shattered_web.png",
    date: "November 18, 2019",
    redirect: ""
  },
  {
    id: 173,
    title: "Berlin 2019 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_berlin2019_champions.png",
    date: "September 8, 2019",
    redirect: ""
  },
  {
    id: 174,
    title: "Berlin 2019 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_berlin2019_legends.png",
    date: "August 23, 2019",
    redirect: ""
  },
  {
    id: 175,
    title: "Berlin 2019 Returning Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_berlin2019_challengers.png",
    date: "August 23, 2019",
    redirect: ""
  },
  {
    id: 176,
    title: "Berlin 2019 Minor Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_berlin2019_contenders.png",
    date: "August 23, 2019",
    redirect: ""
  },
  {
    id: 177,
    title: "Katowice 2019 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2019_champions.png",
    date: "March 3, 2019",
    redirect: ""
  },
  {
    id: 178,
    title: "London 2018 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_london2018_champions.png",
    date: "September 23, 2018",
    redirect: ""
  },
  {
    id: 179,
    title: "London 2018 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_london2018_legends.png",
    date: "September 5, 2018",
    redirect: ""
  },
  {
    id: 180,
    title: "London 2018 Returning Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_london2018_challengers.png",
    date: "September 5, 2018",
    redirect: ""
  },
  {
    id: 181,
    title: "London 2018 Minor Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_london2018_contenders.png",
    date: "September 5, 2018",
    redirect: ""
  },
  {
    id: 182,
    title: "Boston 2018 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_boston2018_champions.png",
    date: "January 28, 2018",
    redirect: ""
  },
  {
    id: 183,
    title: "Boston 2018 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_boston2018_legends.png",
    date: "January 19, 2018",
    redirect: ""
  },
  {
    id: 184,
    title: "Boston 2018 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_boston2018_challengers.png",
    date: "January 19, 2018",
    redirect: ""
  },
  {
    id: 185,
    title: "Krakow 2017 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_krakow2017_champions.png",
    date: "July 23, 2017",
    redirect: ""
  },
  {
    id: 186,
    title: "Krakow 2017 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_krakow2017_legends.png",
    date: "July 16, 2017",
    redirect: ""
  },
  {
    id: 187,
    title: "Krakow 2017 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_krakow2017_challengers.png",
    date: "July 16, 2017",
    redirect: ""
  },
  {
    id: 188,
    title: "Atlanta 2017 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_atlanta2017_champions.png",
    date: "January 29, 2017",
    redirect: ""
  },
  {
    id: 189,
    title: "Atlanta 2017 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_atlanta2017_legends.png",
    date: "January 22, 2017",
    redirect: ""
  },
  {
    id: 190,
    title: "Atlanta 2017 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_atlanta2017_challengers.png",
    date: "January 22, 2017",
    redirect: ""
  },
  {
    id: 191,
    title: "Cologne 2016 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2016_champions.png",
    date: "July 10, 2016",
    redirect: ""
  },
  {
    id: 192,
    title: "Cologne 2016 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2016_legends.png",
    date: "July 5, 2016",
    redirect: ""
  },
  {
    id: 193,
    title: "Cologne 2016 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2016_challengers.png",
    date: "July 5, 2016",
    redirect: ""
  },
  {
    id: 194,
    title: "MLG Columbus 2016 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_mlg2016_champions.png",
    date: "April 3, 2016",
    redirect: ""
  },
  {
    id: 195,
    title: "MLG Columbus 2016 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_mlg2016_legends.png",
    date: "March 29, 2016",
    redirect: ""
  },
  {
    id: 196,
    title: "MLG Columbus 2016 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_mlg2016_challengers.png",
    date: "March 29, 2016",
    redirect: ""
  },
  {
    id: 197,
    title: "Cluj-Napoca 2015 Champions (Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cluj2015_champions.png",
    date: "November 1, 2015",
    redirect: ""
  },
  {
    id: 198,
    title: "Cluj-Napoca 2015 Legends (Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cluj2015_legends.png",
    date: "October 28, 2015",
    redirect: ""
  },
  {
    id: 199,
    title: "Cluj-Napoca 2015 Challengers (Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cluj2015_challengers.png",
    date: "October 28, 2015",
    redirect: ""
  },
  {
    id: 200,
    title: "Cologne 2015 Champions (Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2015_champions.png",
    date: "August 23, 2015",
    redirect: ""
  },
  {
    id: 201,
    title: "Cologne 2015 Legends (Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2015_legends.png",
    date: "August 20, 2015",
    redirect: ""
  },
  {
    id: 202,
    title: "Cologne 2015 Challengers (Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2015_challengers.png",
    date: "August 20, 2015",
    redirect: ""
  },
  {
    id: 203,
    title: "Katowice 2015 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2015_champions.png",
    date: "March 1, 2015",
    redirect: ""
  },
  {
    id: 204,
    title: "Katowice 2015 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2015_legends.png",
    date: "February 26, 2015",
    redirect: ""
  },
  {
    id: 205,
    title: "Katowice 2015 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2015_challengers.png",
    date: "February 26, 2015",
    redirect: ""
  },
  {
    id: 206,
    title: "DreamHack 2014 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_dhw2014_champions.png",
    date: "November 30, 2014",
    redirect: ""
  },
  {
    id: 207,
    title: "DreamHack 2014 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_dhw2014_legends.png",
    date: "November 26, 2014",
    redirect: ""
  },
  {
    id: 208,
    title: "DreamHack 2014 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_dhw2014_challengers.png",
    date: "November 26, 2014",
    redirect: ""
  },
  {
    id: 209,
    title: "Cologne 2014 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2014_champions.png",
    date: "August 17, 2014",
    redirect: ""
  },
  {
    id: 210,
    title: "Cologne 2014 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2014_legends.png",
    date: "August 14, 2014",
    redirect: ""
  },
  {
    id: 211,
    title: "Cologne 2014 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_cologne2014_challengers.png",
    date: "August 14, 2014",
    redirect: ""
  },
  {
    id: 212,
    title: "Katowice 2014 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2014_champions.png",
    date: "March 15, 2014",
    redirect: ""
  },
  {
    id: 213,
    title: "Katowice 2014 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2014_legends.png",
    date: "March 5, 2014",
    redirect: ""
  },
  {
    id: 214,
    title: "Katowice 2014 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_katowice2014_challengers.png",
    date: "March 5, 2014",
    redirect: ""
  },
  {
    id: 215,
    title: "Rio 2022 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_champions.png",
    date: "November 13, 2022",
    redirect: ""
  },
  {
    id: 216,
    title: "Rio 2022 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_legends.png",
    date: "October 21, 2022",
    redirect: ""
  },
  {
    id: 217,
    title: "Rio 2022 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_challengers.png",
    date: "October 21, 2022",
    redirect: ""
  },
  {
    id: 218,
    title: "Rio 2022 Contenders (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_rio2022_contenders.png",
    date: "October 21, 2022",
    redirect: ""
  },
  {
    id: 219,
    title: "Paris 2023 Champions (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_paris2023_champions.png",
    date: "May 21, 2023",
    redirect: ""
  },
  {
    id: 220,
    title: "Paris 2023 Legends (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_paris2023_legends.png",
    date: "May 21, 2023",
    redirect: ""
  },
  {
    id: 221,
    title: "Paris 2023 Challengers (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_paris2023_challengers.png",
    date: "May 21, 2023",
    redirect: ""
  },
  {
    id: 222,
    title: "Paris 2023 Contenders (Holo/Foil)",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_paris2023_contenders.png",
    date: "May 21, 2023",
    redirect: ""
  },
  {
    id: 223,
    title: "Antwerp 2022 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_champions_autograph.png",
    date: "May 21, 2022",
    redirect: ""
  },
  {
    id: 224,
    title: "Antwerp 2022 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_legends_autograph.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 225,
    title: "Antwerp 2022 Challengers Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_challengers_autograph.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 226,
    title: "Antwerp 2022 Contenders Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_antwerp2022_contenders_autograph.png",
    date: "May 9, 2022",
    redirect: ""
  },
  {
    id: 227,
    title: "Stockholm 2021 Champions Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_champions_autograph.png",
    date: "November 7, 2021",
    redirect: ""
  },
  {
    id: 228,
    title: "Stockholm 2021 Legends Autograph Capsule",
    image: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_sticker_pack_stockholm2021_legends_autograph.png",
    date: "October 26, 2021",
    redirect: ""
  }
];

const collections = [
  {
    id: 1,
    title: "The Gallery Collection",
    image: collection_gallary,
    date: "October 1, 2024",
    redirect: ""
  },
  {
    id: 2,
    title: "The Overpass 2024 Collection",
    image: collection_overpass,
    date: "October 1, 2024",
    redirect: ""
  },
  {
    id: 3,
    title: "The Graphic Design Collection",
    image: collection_graphic_design,
    date: "October 1, 2024",
    redirect: ""
  },
  {
    id: 4,
    title: "The Sport & Field Collection",
    image: collection_sport_field,
    date: "October 1, 2024",
    redirect: ""
  },
  {
    id: 5,
    title: "The Revolution Collection",
    image: collection_the_revolution,
    date: "February 10, 2023",
    redirect: ""
  },
  {
    id: 6,
    title: "The Anubis Collection",
    image: collection_anubis,
    date: "April 25, 2023",
    redirect: ""
  },
  {
    id: 7,
    title: "The Kilowatt Collection",
    image: collection_kilowatt,
    date: "February 8, 2024",
    redirect: ""
  },
  {
    id: 8,
    title: "Limited Edition Item",
    image: collection_limited_1,
    date: "October 1, 2024",
    redirect: ""
  },
  {
    id: 9,
    title: "The Recoil Collection",
    image: collection_recoil,
    date: "July 1, 2022",
    redirect: ""
  },
  {
    id: 10,
    title: "The Dreams & Nightmares Collection",
    image: collection_dreams_nightmares,
    date: "January 21, 2022",
    redirect: ""
  },
  {
    id: 11,
    title: "The 2021 Train Collection",
    image: collection_train_2021,
    date: "September 22, 2021",
    redirect: ""
  },
  {
    id: 12,
    title: "The 2021 Dust 2 Collection",
    image: collection_dust_2_2021,
    date: "September 22, 2021",
    redirect: ""
  },
  {
    id: 13,
    title: "The 2021 Mirage Collection",
    image: collection_mirage_2021,
    date: "September 22, 2021",
    redirect: ""
  },
  {
    id: 14,
    title: "The Snakebite Collection",
    image: collection_snakebite,
    date: "May 3, 2021",
    redirect: ""
  },
  {
    id: 15,
    title: "The Operation Riptide Collection",
    image: collection_operation_riptide,
    date: "September 22, 2021",
    redirect: ""
  },
  {
    id: 16,
    title: "The 2021 Vertigo Collection",
    image: collection_vertigo_2021,
    date: "September 22, 2021",
    redirect: ""
  },
  {
    id: 17,
    title: "The Havoc Collection",
    image: collection_havoc,
    date: "December 3, 2020",
    redirect: ""
  },
  {
    id: 18,
    title: "The Ancient Collection",
    image: collection_ancient,
    date: "December 3, 2020",
    redirect: ""
  },
  {
    id: 19,
    title: "The Control Collection",
    image: collection_control,
    date: "December 3, 2020",
    redirect: ""
  },
  {
    id: 20,
    title: "The Operation Broken Fang Collection",
    image: collection_operation_broken_fang,
    date: "December 3, 2020",
    redirect: ""
  },
  {
    id: 21,
    title: "The St. Marc Collection",
    image: collection_st_marc,
    date: "December 3, 2020",
    redirect: ""
  },
  {
    id: 22,
    title: "The Canals Collection",
    image: collection_canals,
    date: "March 15, 2017",
    redirect: ""
  },
  {
    id: 23,
    title: "The Prisma 2 Collection",
    image: collection_prisma_2,
    date: "March 31, 2020",
    redirect: ""
  },
  {
    id: 24,
    title: "The Fracture Collection",
    image: collection_fracture,
    date: "August 7, 2020",
    redirect: ""
  },
  {
    id: 25,
    title: "The X-Ray Collection",
    image: collection_x_ray,
    date: "November 18, 2019",
    redirect: ""
  },
  {
    id: 26,
    title: "The CS20 Collection",
    image: collection_cs20,
    date: "October 18, 2019",
    redirect: ""
  },
  {
    id: 27,
    title: "The Shattered Web Collection",
    image: collection_shattered_web,
    date: "November 18, 2019",
    redirect: ""
  },
  {
    id: 28,
    title: "The Norse Collection",
    image: collection_norse,
    date: "July 31, 2019",
    redirect: ""
  },
  {
    id: 29,
    title: "The Prisma Collection",
    image: collection_prisma,
    date: "March 13, 2019",
    redirect: ""
  },
  {
    id: 30,
    title: "The Clutch Collection",
    image: collection_clutch,
    date: "February 15, 2018",
    redirect: ""
  },
  {
    id: 31,
    title: "The Blacksite Collection",
    image: collection_blacksite,
    date: "December 6, 2018",
    redirect: ""
  },
  {
    id: 32,
    title: "The Danger Zone Collection",
    image: collection_danger_zone,
    date: "December 6, 2018",
    redirect: ""
  },
  {
    id: 33,
    title: "The 2018 Nuke Collection",
    image: collection_2018_nuke_collection,
    date: "October 1, 2018",
    redirect: ""
  },
  {
    id: 34,
    title: "The 2018 Inferno Collection",
    image: collection_2018_inferno_collection,
    date: "October 1, 2018",
    redirect: ""
  },
  {
    id: 35,
    title: "The Horizon Collection",
    image: collection_horizon_collection,
    date: "July 2, 2018",
    redirect: ""
  },
  {
    id: 36,
    title: "The Spectrum 2 Collection",
    image: collection_spectrum_2_collection,
    date: "September 14, 2017",
    redirect: ""
  },
  {
    id: 37,
    title: "The Operation Hydra Collection",
    image: collection_operation_hydra_collection,
    date: "May 23, 2017",
    redirect: ""
  },
  {
    id: 38,
    title: "The Spectrum Collection",
    image: collection_spectrum_collection,
    date: "March 15, 2017",
    redirect: ""
  },
  {
    id: 39,
    title: "The Glove Collection",
    image: collection_glove_collection,
    date: "November 28, 2016",
    redirect: ""
  },
  {
    id: 40,
    title: "The Gamma 2 Collection",
    image: collection_gamma_2_collection,
    date: "August 18, 2016",
    redirect: ""
  },
  {
    id: 41,
    title: "The Gamma Collection",
    image: collection_gamma_collection,
    date: "June 15, 2016",
    redirect: ""
  },
  {
    id: 42,
    title: "The Chroma 3 Collection",
    image: collection_chroma_3_collection,
    date: "April 27, 2016",
    redirect: ""
  },
  {
    id: 43,
    title: "The Wildfire Collection",
    image: collection_wildfire_collection,
    date: "February 17, 2016",
    redirect: ""
  },
  {
    id: 44,
    title: "The Revolver Case Collection",
    image: collection_revolver_case_collection,
    date: "December 8, 2015",
    redirect: ""
  },
  {
    id: 45,
    title: "The Shadow Collection",
    image: collection_shadow_collection,
    date: "September 17, 2015",
    redirect: ""
  },
  {
    id: 46,
    title: "The Rising Sun Collection",
    image: collection_rising_sun_collection,
    date: "May 26, 2015",
    redirect: ""
  },
  {
    id: 47,
    title: "The Gods & Monsters Collection",
    image: collection_gods_and_monsters_collection,
    date: "May 26, 2015",
    redirect: ""
  },
  {
    id: 48,
    title: "The Chop Shop Collection",
    image: collection_chop_shop_collection,
    date: "May 26, 2015",
    redirect: ""
  },
  {
    id: 49,
    title: "The Falchion Collection",
    image: collection_falchion_collection,
    date: "May 26, 2015",
    redirect: ""
  },
  {
    id: 50,
    title: "The Chroma 2 Collection",
    image: collection_chroma_2_collection,
    date: "April 15, 2015",
    redirect: ""
  },
  {
    id: 51,
    title: "The Chroma Collection",
    image: collection_chroma_collection,
    date: "January 8, 2015",
    redirect: ""
  },
  {
    id: 52,
    title: "The Vanguard Collection",
    image: collection_vanguard_collection,
    date: "November 11, 2014",
    redirect: ""
  },
  {
    id: 53,
    title: "The Cache Collection",
    image: collection_cache_collection,
    date: "July 1, 2014",
    redirect: ""
  },
  {
    id: 54,
    title: "The Esports 2014 Summer Collection",
    image: collection_esports_2014_summer_collection,
    date: "July 1, 2014",
    redirect: ""
  },
  {
    id: 55,
    title: "The Breakout Collection",
    image: collection_breakout_collection,
    date: "July 1, 2014",
    redirect: ""
  },
  {
    id: 56,
    title: "The Baggage Collection",
    image: collection_baggage_collection,
    date: "May 1, 2014",
    redirect: ""
  },
  {
    id: 57,
    title: "The Overpass Collection",
    image: collection_overpass_collection,
    date: "December 18, 2013",
    redirect: ""
  },
  {
    id: 58,
    title: "The Cobblestone Collection",
    image: collection_cobblestone_collection,
    date: "December 18, 2013",
    redirect: ""
  },
  {
    id: 59,
    title: "The Bank Collection",
    image: collection_bank_collection,
    date: "December 18, 2013",
    redirect: ""
  },
  {
    id: 60,
    title: "The Huntsman Collection",
    image: collection_huntsman_collection,
    date: "May 1, 2014",
    redirect: ""
  },
  {
    id: 61,
    title: "The Phoenix Collection",
    image: collection_phoenix_collection,
    date: "February 20, 2014",
    redirect: ""
  },
  {
    id: 62,
    title: "The Arms Deal 3 Collection",
    image: collection_arms_deal_3_collection,
    date: "January 9, 2014",
    redirect: ""
  },
  {
    id: 63,
    title: "The Esports 2013 Winter Collection",
    image: collection_esports_2013_winter_collection,
    date: "December 18, 2013",
    redirect: ""
  },
  {
    id: 64,
    title: "The Winter Offensive Collection",
    image: collection_winter_offensive_collection,
    date: "December 18, 2013",
    redirect: ""
  },
  {
    id: 65,
    title: "The Italy Collection",
    image: collection_italy_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 66,
    title: "The Mirage Collection",
    image: collection_mirage_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 67,
    title: "The Safehouse Collection",
    image: collection_safehouse_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 68,
    title: "The Dust 2 Collection",
    image: collection_dust_2_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 69,
    title: "The Lake Collection",
    image: collection_lake_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 70,
    title: "The Train Collection",
    image: collection_train_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 71,
    title: "The Arms Deal 2 Collection",
    image: collection_arms_deal_2_collection,
    date: "November 8, 2013",
    redirect: ""
  },
  {
    id: 72,
    title: "The Alpha Collection",
    image: collection_alpha_collection,
    date: "September 19, 2013",
    redirect: ""
  },
  {
    id: 73,
    title: "The Bravo Collection",
    image: collection_bravo_collection,
    date: "September 19, 2013",
    redirect: ""
  },
  {
    id: 74,
    title: "The Assault Collection",
    image: collection_assault_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 75,
    title: "The Dust Collection",
    image: collection_dust_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 76,
    title: "The Office Collection",
    image: collection_office_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 77,
    title: "The Nuke Collection",
    image: collection_nuke_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 78,
    title: "The Aztec Collection",
    image: collection_aztec_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 79,
    title: "The Inferno Collection",
    image: collection_inferno_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 80,
    title: "The Arms Deal Collection",
    image: collection_arms_deal_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 81,
    title: "The Militia Collection",
    image: collection_militia_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 82,
    title: "The Vertigo Collection",
    image: collection_vertigo_collection,
    date: "August 14, 2013",
    redirect: ""
  },
  {
    id: 83,
    title: "The Esports 2013 Collection",
    image: collection_esports_2013_collection,
    date: "August 14, 2013",
    redirect: ""
  }
];

export default function Wiki() {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const [isOpenCapsules, setIsOpenCapsules] = useState(false);
  const [initialCount, setInitialCount] = useState(8);

  // Функция для расчета количества карточек на основе ширины экрана
  const calculateInitialCount = () => {
    const width = window.innerWidth;
    if (width < 678) return 2; // mobile
    if (width < 768) return 3; // mobile
    if (width < 948) return 2; // mobile
    if (width < 1166) return 3; // mobile
    if (width < 1384) return 4; // tablet
    if (width < 1602) return 5; // small laptop
    return 6; // desktop and larger
  };

  // Обновляем количество при изменении размера окна
  useEffect(() => {
    const handleResize = () => {
      if (!isOpen) { // Обновляем только если список свёрнут
        setInitialCount(calculateInitialCount());
      }
    };

    // Устанавливаем начальное значение
    setInitialCount(calculateInitialCount());

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isOpen]);

  const visibleCollections = isOpen ? collections : collections.slice(0, initialCount);
  const visibleCapsules = isOpenCapsules ? sticker_collection : sticker_collection.slice(0, initialCount);

  return (
    <div className="flex flex-col w-full">
      <div className="py-6 bg-dark-1 text-light-2 w-full">
        <div className="container mx-auto text-center px-4">
          <h2 className="text-4xl font-bold mb-10 text-white">COLLECTIONS</h2>
          <div
            className="grid w-full gap-4"
            style={{
              gridTemplateColumns: 'repeat(auto-fill, minmax(210px, 1fr))',
              maxWidth: '100%'
            }}
          >
            {visibleCollections.map((collection) => (
              <div
                key={collection.id}
                className="collection-card space-y-2 p-3 h-full cursor-pointer"
                onClick={() => collection.redirect && navigate(collection.redirect)}
              >
                <div className="bg-dark-2 rounded-xl overflow-hidden shadow-lg hover:bg-dark-3 transition-colors duration-200">
                  <div className="w-[175px] h-[175px] relative overflow-hidden mx-auto">
                    <img
                      className="w-full h-full object-contain p-4"
                      alt={collection.title}
                      src={collection.image}
                      loading="lazy"
                    />
                  </div>

                  <div className="p-5">
                    <h3 className="text-lg font-semibold text-white mb-2 line-clamp-2 min-h-[3.5rem]">
                      {collection.title}
                    </h3>
                    <div className="h-px bg-gray-700 my-3" />
                    <div className="text-gray-400 text-sm">
                      {collection.date}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {collections.length > initialCount && (
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="mt-8 inline-flex items-center gap-2 px-6 py-3 bg-dark-2 text-white rounded-lg hover:bg-primary-500 transition-colors duration-200"
            >
              <span>{isOpen ? 'Show Less' : 'Show More'}</span>
              {isOpen ? <UpOutlined className="h-5 w-5" /> : <DownOutlined className="h-5 w-5" />}
            </button>
          )}
        </div>
      </div>

      <div className="py-6 bg-dark-1 text-light-2 w-full border-t border-gray-800">
        <div className="container mx-auto text-center px-4">
          <h2 className="text-4xl font-bold mb-10 text-white">CAPSULES</h2>
          <div
            className="grid w-full gap-4"
            style={{
              gridTemplateColumns: 'repeat(auto-fill, minmax(210px, 1fr))',
              maxWidth: '100%'
            }}
          >
            {visibleCapsules.map((capsule) => (
              <div
                key={capsule.id}
                className="collection-card space-y-2 p-3 h-full cursor-pointer"
                onClick={() => capsule.redirect && navigate(capsule.redirect)}
              >
                <div className="bg-dark-2 rounded-xl overflow-hidden shadow-lg hover:bg-dark-3 transition-colors duration-200">
                  <div className="w-[175px] h-[175px] relative overflow-hidden mx-auto">
                    <img
                      className="w-full h-full object-contain p-4"
                      alt={capsule.title}
                      src={capsule.image}
                      loading="lazy"
                    />
                  </div>

                  <div className="p-5">
                    <h3 className="text-lg font-semibold text-white mb-2 line-clamp-2 min-h-[3.5rem]">
                      {capsule.title}
                    </h3>
                    <div className="h-px bg-gray-700 my-3" />
                    <div className="text-gray-400 text-sm">
                      {capsule.date}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {sticker_collection.length > initialCount && (
            <button
              onClick={() => setIsOpenCapsules(!isOpenCapsules)}
              className="mt-8 inline-flex items-center gap-2 px-6 py-3 bg-dark-2 text-white rounded-lg hover:bg-primary-500 transition-colors duration-200"
            >
              <span>{isOpenCapsules ? 'Show Less' : 'Show More'}</span>
              {isOpenCapsules ? <UpOutlined className="h-5 w-5" /> : <DownOutlined className="h-5 w-5" />}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
