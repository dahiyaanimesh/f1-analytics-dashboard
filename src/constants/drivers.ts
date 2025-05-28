// Comprehensive F1 Driver List (2018-2025)
export interface Driver {
  code: string;
  name: string;
  seasons: number[];
  teams?: string[];
}

export const F1_DRIVERS: Driver[] = [
  // Current 2025 Grid
  { code: 'VER', name: 'Max Verstappen', seasons: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], teams: ['Red Bull Racing'] },
  { code: 'LEC', name: 'Charles Leclerc', seasons: [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], teams: ['Ferrari'] },
  { code: 'HAM', name: 'Lewis Hamilton', seasons: [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], teams: ['Ferrari'] },
  { code: 'RUS', name: 'George Russell', seasons: [2019, 2020, 2021, 2022, 2023, 2024, 2025], teams: ['Mercedes'] },
  { code: 'NOR', name: 'Lando Norris', seasons: [2019, 2020, 2021, 2022, 2023, 2024, 2025], teams: ['McLaren'] },
  { code: 'PIA', name: 'Oscar Piastri', seasons: [2023, 2024, 2025], teams: ['McLaren'] },
  { code: 'SAI', name: 'Carlos Sainz', seasons: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], teams: ['Williams'] },
  { code: 'PER', name: 'Sergio Perez', seasons: [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024], teams: ['Red Bull Racing'] },
  { code: 'COL', name: 'Franco Colapinto', seasons: [2024, 2025], teams: ['Alpine'] },
  { code: 'ALO', name: 'Fernando Alonso', seasons: [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2022, 2023, 2024, 2025], teams: ['Aston Martin'] },
  { code: 'STR', name: 'Lance Stroll', seasons: [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], teams: ['Aston Martin'] },
  { code: 'TSU', name: 'Yuki Tsunoda', seasons: [2021, 2022, 2023, 2024, 2025], teams: ['RB'] },
  { code: 'LAW', name: 'Liam Lawson', seasons: [2023, 2024, 2025], teams: ['RB'] },
  { code: 'HUL', name: 'Nico Hulkenberg', seasons: [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025], teams: ['Haas'] },
  { code: 'MAG', name: 'Kevin Magnussen', seasons: [2014, 2015, 2016, 2017, 2022, 2023, 2024, 2025], teams: ['Haas'] },
  { code: 'ALB', name: 'Alexander Albon', seasons: [2019, 2020, 2021, 2022, 2023, 2024, 2025], teams: ['Williams'] },
  { code: 'GAS', name: 'Pierre Gasly', seasons: [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], teams: ['Alpine'] },
  { code: 'OCO', name: 'Esteban Ocon', seasons: [2016, 2017, 2018, 2020, 2021, 2022, 2023, 2024, 2025], teams: ['Alpine'] },
  { code: 'BOT', name: 'Valtteri Bottas', seasons: [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], teams: ['Kick Sauber'] },
  { code: 'ZHO', name: 'Zhou Guanyu', seasons: [2022, 2023, 2024, 2025], teams: ['Kick Sauber'] },
  { code: 'BEA', name: 'Oliver Bearman', seasons: [2024, 2025], teams: ['Haas'] },

  // Recent/Former Drivers (2018-2024)
  { code: 'RIC', name: 'Daniel Ricciardo', seasons: [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024], teams: ['Red Bull', 'Renault', 'McLaren', 'AlphaTauri'] },
  { code: 'VET', name: 'Sebastian Vettel', seasons: [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022], teams: ['Aston Martin', 'Ferrari', 'Red Bull'] },
  { code: 'RAI', name: 'Kimi Raikkonen', seasons: [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021], teams: ['Alfa Romeo', 'Ferrari', 'McLaren'] },
  { code: 'MSC', name: 'Mick Schumacher', seasons: [2021, 2022], teams: ['Haas'] },
  { code: 'LAT', name: 'Nicholas Latifi', seasons: [2020, 2021, 2022], teams: ['Williams'] },
  { code: 'MAZ', name: 'Nikita Mazepin', seasons: [2021], teams: ['Haas'] },
  { code: 'GIO', name: 'Antonio Giovinazzi', seasons: [2017, 2019, 2020, 2021], teams: ['Alfa Romeo'] },
  { code: 'DEV', name: 'Nyck de Vries', seasons: [2022, 2023], teams: ['AlphaTauri', 'Williams'] },
  { code: 'SAR', name: 'Logan Sargeant', seasons: [2023, 2024], teams: ['Williams'] },
  { code: 'KVY', name: 'Daniil Kvyat', seasons: [2014, 2015, 2016, 2017, 2019, 2020], teams: ['AlphaTauri', 'Red Bull'] },
  { code: 'GRO', name: 'Romain Grosjean', seasons: [2009, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020], teams: ['Haas', 'Lotus'] },
  { code: 'FIT', name: 'Pietro Fittipaldi', seasons: [2020], teams: ['Haas'] },
  { code: 'AIT', name: 'Jack Aitken', seasons: [2020], teams: ['Williams'] },
  { code: 'VAN', name: 'Stoffel Vandoorne', seasons: [2016, 2017, 2018], teams: ['McLaren'] },
  { code: 'ERE', name: 'Marcus Ericsson', seasons: [2014, 2015, 2016, 2017, 2018], teams: ['Sauber'] },
  { code: 'WEH', name: 'Pascal Wehrlein', seasons: [2016, 2017], teams: ['Manor', 'Sauber'] },
  { code: 'SIR', name: 'Sergey Sirotkin', seasons: [2018], teams: ['Williams'] },
  { code: 'HAR', name: 'Brendon Hartley', seasons: [2017, 2018], teams: ['Toro Rosso'] },
];

export const YEARS = [2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018];

export const getDriversForYear = (year: number): Driver[] => {
  return F1_DRIVERS.filter(driver => driver.seasons.includes(year));
};

export const getAllDrivers = (): Driver[] => {
  return F1_DRIVERS;
};