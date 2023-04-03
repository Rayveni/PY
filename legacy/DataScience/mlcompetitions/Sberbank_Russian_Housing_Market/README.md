# Task description  
Housing costs demand a significant investment from both consumers and developers. And when it comes to planning a budget—whether personal or corporate—the last thing anyone needs is uncertainty about one of their biggets expenses. Sberbank, Russia’s oldest and largest bank, helps their customers by making predictions about realty prices so renters, developers, and lenders are more confident when they sign a lease or purchase a building.

Although the housing market is relatively stable in Russia, the country’s volatile economy makes forecasting prices as a function of apartment characteristics a unique challenge. Complex interactions between housing features such as number of bedrooms and location are enough to make pricing predictions complicated. Adding an unstable economy to the mix means Sberbank and their customers need more than simple regression models in their arsenal.

In this competition, Sberbank is challenging Kagglers to develop algorithms which use a broad spectrum of features to predict realty prices. Competitors will rely on a rich dataset that includes housing data and macroeconomic patterns. An accurate forecasting model will allow Sberbank to provide more certainty to their customers in an uncertain economy. <br>  **train.csv** and **test.csv**:
 

  **feature** | **description**
  ------------- | -------------|
price_doc| sale price (this is the target variable)
id| transaction id
timestamp| date of transaction
full_sq| total area in square meters, including loggias, balconies and other non-residential areas
life_sq| living area in square meters, excluding loggias, balconies and other non-residential areas
floor| for apartments, floor of the building
max_floor| number of floors in the building
material| wall material
build_year| year built
num_room| number of living rooms
kitch_sq| kitchen area
state| apartment condition
product_type| owner-occupier purchase or investment
sub_area| name of the district

The dataset also includes a collection of features about each property's surrounding neighbourhood, and some features that are constant across each sub area (known as a Raion). Most of the feature names are self explanatory, with the following notes. See below for a complete list.

  **feature** | **description**
  ------------- | -------------|
full_all| subarea population
male_f, female_f| subarea population by gender
young_*| population younger than working age
work_*| working-age population
ekder_*| retirement-age population
n_m_{all/male/female}| population between n and m years old
build_count_*| buildings in the subarea by construction type or year
x_count_500| the number of x within 500m of the property
x_part_500| the share of x within 500m of the property
_sqm_| square meters
cafe_count_d_price_p| number of cafes within d meters of the property that have an average bill under p RUB
trc_| shopping malls
prom_| industrial zones
green_| green zones
metro_| subway
_avto_| distances by car
mkad_| Moscow Circle Auto Road
ttk_| Third Transport Ring
sadovoe_| Garden Ring
bulvar_ring_| Boulevard Ring
kremlin_| City center
zd_vokzaly_| Train station
oil_chemistry_| Dirty industry
ts_| Power plant

### Complete description of neighbourhood features
<details>
  <summary>hide/show  **click**</summary>
 
 <table border="1">

   <tr>
    <th>feature</th>
    <th>description</th>

   </tr>
<tr><td>area_m</td><td>Area mun. area, sq.m.</td></tr>
<tr><td>raion_popul</td><td>Number of municipality population. district</td></tr>
<tr><td>green_zone_part</td><td>Proportion of area of â€‹â€‹greenery in the total area</td></tr>
<tr><td>indust_part</td><td>Share of industrial zones in area of â€‹â€‹the total area</td></tr>
<tr><td>children_preschool</td><td>Number of pre-school age population</td></tr>
<tr><td>preschool_quota</td><td>Number of seats in pre-school organizations</td></tr>
<tr><td>preschool_education_centers_raion</td><td>Number of pre-school  institutions</td></tr>
<tr><td>children_school</td><td>Population of school-age children</td></tr>
<tr><td>school_quota</td><td>Number of high school seats in area</td></tr>
<tr><td>school_education_centers_raion</td><td>Number of  high school institutions</td></tr>
<tr><td>school_education_centers_top_20_raion</td><td>Number of high schools of the top 20 best schools in Moscow</td></tr>
<tr><td>hospital_beds_raion</td><td>Number of hospital beds for the district</td></tr>
<tr><td>healthcare_centers_raion</td><td>Number of healthcare centers in district</td></tr>
<tr><td>university_top_20_raion</td><td>Number of higher education institutions in the top ten ranking of the Federal rank</td></tr>
<tr><td>sport_objects_raion</td><td>Number of higher education institutions</td></tr>
<tr><td>additional_education_raion</td><td>Number of additional education organizations</td></tr>
<tr><td>culture_objects_top_25</td><td>Presence of the key objects of cultural heritage (significant objects for the level of the RF constituent entities, city)</td></tr>
<tr><td>culture_objects_top_25_raion</td><td>Number of  objects of cultural heritage</td></tr>
<tr><td>shopping_centers_raion</td><td>Number of malls and shopping centres in district</td></tr>
<tr><td>office_raion</td><td>Number of malls and shopping centres in district</td></tr>
<tr><td>thermal_power_plant_raion</td><td>Presence of thermal power station in district</td></tr>
<tr><td>incineration_raion</td><td>Presence of incinerators</td></tr>
<tr><td>oil_chemistry_raion</td><td>Presence of dirty industries</td></tr>
<tr><td>radiation_raion</td><td>Presence of radioactive waste disposal</td></tr>
<tr><td>railroad_terminal_raion</td><td>Presence of the railroad terminal in district</td></tr>
<tr><td>big_market_raion</td><td>Presence of large grocery / wholesale markets</td></tr>
<tr><td>nuclear_reactor_raion</td><td>Presence of existing nuclear reactors</td></tr>
<tr><td>detention_facility_raion</td><td>Presence of detention centers, prisons</td></tr>
<tr><td>full_all</td><td>Total number of  population in the municipality</td></tr>
<tr><td>male_f</td><td>Male population</td></tr>
<tr><td>female_f</td><td>Female population</td></tr>
<tr><td>young_all</td><td>Population younger than working age</td></tr>
<tr><td>young_male</td><td>Male population younger than working age </td></tr>
<tr><td>young_female</td><td>Feale population younger than working age </td></tr>
<tr><td>work_all</td><td>Working-age population</td></tr>
<tr><td>work_male</td><td>Male working-age population</td></tr>
<tr><td>work_female</td><td>Female working-age population</td></tr>
<tr><td>ekder_all</td><td>Population older than  working age</td></tr>
<tr><td>ekder_male</td><td>Male population older than  working age</td></tr>
<tr><td>ekder_female</td><td>Female population older than  working age</td></tr>
<tr><td>0_6_all</td><td>Population aged 0-6</td></tr>
<tr><td>0_6_male</td><td>Male population aged 0-7</td></tr>
<tr><td>0_6_female</td><td>Female population aged 0-8</td></tr>
<tr><td>7_14_all</td><td>Population aged  7-14</td></tr>
<tr><td>7_14_male</td><td>Male population aged 7-14</td></tr>
<tr><td>7_14_female</td><td>Female population aged 7-14</td></tr>
<tr><td>0_17_all</td><td>Population aged 0-17</td></tr>
<tr><td>0_17_male</td><td>Male population aged 0-17</td></tr>
<tr><td>0_17_female</td><td>Female population aged 0-17</td></tr>
<tr><td>16_29_all</td><td>Population aged 16-19</td></tr>
<tr><td>16_29_male</td><td>Male population aged 16-19</td></tr>
<tr><td>16_29_female</td><td>Female population aged 16-19</td></tr>
<tr><td>0_13_all</td><td>Population aged 0-13</td></tr>
<tr><td>0_13_male</td><td>Male population aged 0-13</td></tr>
<tr><td>0_13_female</td><td>Female population aged 0-13</td></tr>
<tr><td>raion_build_count_with_material_info</td><td>Number of building with material info in district</td></tr>
<tr><td>build_count_block</td><td>Share of block buildings</td></tr>
<tr><td>build_count_wood</td><td>Share of wood buildings</td></tr>
<tr><td>build_count_frame</td><td>Share of frame buildings</td></tr>
<tr><td>build_count_brick</td><td>Share of brick buildings</td></tr>
<tr><td>build_count_monolith</td><td>Share of monolith buildings</td></tr>
<tr><td>build_count_panel</td><td>Share of panel buildings</td></tr>
<tr><td>build_count_foam</td><td>Share of foam buildings</td></tr>
<tr><td>build_count_slag</td><td>Share of slag buildings</td></tr>
<tr><td>build_count_mix</td><td>Share of mixed buildings</td></tr>
<tr><td>raion_build_count_with_builddate_info</td><td>Number of building with build year info in district</td></tr>
<tr><td>build_count_before_1920</td><td>Share of before_1920 buildings</td></tr>
<tr><td>build_count_1921-1945</td><td>Share of 1921-1945 buildings</td></tr>
<tr><td>build_count_1946-1970</td><td>Share of 1946-1970 buildings</td></tr>
<tr><td>build_count_1971-1995</td><td>Share of 1971-1995 buildings</td></tr>
<tr><td>build_count_after_1995</td><td>Share of after_1995 buildings</td></tr>
<tr><td>7_14_male</td><td>Male population aged 7-14</td></tr>
<tr><td>7_14_female</td><td>Female population aged 7-14</td></tr>
<tr><td>0_17_all</td><td>Population aged 0-17</td></tr>
<tr><td>0_17_male</td><td>Male population aged 0-17</td></tr>
<tr><td>0_17_female</td><td>Female population aged 0-17</td></tr>
<tr><td>16_29_all</td><td>Population aged 16-19</td></tr>
<tr><td>16_29_male</td><td>Male population aged 16-19</td></tr>
<tr><td>16_29_female</td><td>Female population aged 16-19</td></tr>
<tr><td>0_13_all</td><td>Population aged 0-13</td></tr>
<tr><td>0_13_male</td><td>Male population aged 0-13</td></tr>
<tr><td>0_13_female</td><td>Female population aged 0-13</td></tr>
<tr><td>metro_min_avto</td><td>Time to subway by car, min.</td></tr>
<tr><td>metro_km_avto</td><td>Distance to subway by car, km</td></tr>
<tr><td>metro_min_walk</td><td>Time to metro by foot</td></tr>
<tr><td>metro_km_walk</td><td>Distance to the metro, km</td></tr>
<tr><td>kindergarten_km</td><td>Distance to kindergarten</td></tr>
<tr><td>school_km</td><td>Distance to high school </td></tr>
<tr><td>park_km</td><td>Distance to park</td></tr>
<tr><td>green_zone_km</td><td>Distance to green zone</td></tr>
<tr><td>industrial_zone_km</td><td>Distance to industrial zone</td></tr>
<tr><td>water_treatment_km</td><td>Distance to water treatment</td></tr>
<tr><td>cemetery_km</td><td>Distance to the cemetery</td></tr>
<tr><td>incineration_km</td><td>Distance to the incineration</td></tr>
<tr><td>railroad_station_walk_km</td><td>Distance to the railroad station (walk)</td></tr>
<tr><td>railroad_station_walk_min</td><td>Time to the railroad station (walk)</td></tr>
<tr><td>ID_railroad_station_walk</td><td>Nearest railroad station id (walk)</td></tr>
<tr><td>railroad_station_avto_km</td><td>Distance to the railroad station (avto)</td></tr>
<tr><td>railroad_station_avto_min</td><td>Time to the railroad station (avto)</td></tr>
<tr><td>ID_railroad_station_avto</td><td>Nearest railroad station id (avto)</td></tr>
<tr><td>public_transport_station_km</td><td>Distance to the public transport station (walk)</td></tr>
<tr><td>public_transport_station_min_walk</td><td>Time to the public transport station (walk)</td></tr>
<tr><td>water_km</td><td>Distance to the water reservoir / river</td></tr>
<tr><td>water_1line</td><td>First line to the river (150 m)</td></tr>
<tr><td>mkad_km</td><td>Distance to MKAD (Moscow Circle Auto Road)</td></tr>
<tr><td>ttk_km</td><td>Distance to the TTC (Third Transport Ring)</td></tr>
<tr><td>sadovoe_km</td><td>Distance to the Garden Ring</td></tr>
<tr><td>bulvar_ring_km</td><td>The distance to the Boulevard Ring</td></tr>
<tr><td>kremlin_km</td><td>Distance to the city center (Kremlin)</td></tr>
<tr><td>big_road1_km</td><td>Distance to Nearest major road</td></tr>
<tr><td>ID_big_road1</td><td>Nearest big road id</td></tr>
<tr><td>big_road1_1line</td><td>First line to the road (100 m for highwys, 250 m to MKAD)</td></tr>
<tr><td>big_road2_km</td><td>The distance to next distant major road</td></tr>
<tr><td>ID_big_road2</td><td>2nd nearest big road id</td></tr>
<tr><td>railroad_km</td><td>Distance to the railway / Moscow Central Ring / open areas Underground</td></tr>
<tr><td>railroad_1line</td><td>First line to the railway (100 m)</td></tr>
<tr><td>zd_vokzaly_avto_km</td><td>Distance to train station</td></tr>
<tr><td>ID_railroad_terminal</td><td>Nearest railroad terminal id</td></tr>
<tr><td>bus_terminal_avto_km</td><td>Distance to bus terminal (avto)</td></tr>
<tr><td>ID_bus_terminal</td><td>Nearest bus terminal id</td></tr>
<tr><td>oil_chemistry_km</td><td>Distance to dirty industries</td></tr>
<tr><td>nuclear_reactor_km</td><td>Distance to nuclear reactor</td></tr>
<tr><td>radiation_km</td><td>Distance to burial of radioactive waste</td></tr>
<tr><td>power_transmission_line_km</td><td>Distance to power transmission line</td></tr>
<tr><td>thermal_power_plant_km</td><td>Distance to thermal power plant</td></tr>
<tr><td>ts_km</td><td>Distance to power station</td></tr>
<tr><td>big_market_km</td><td>Distance to grocery / wholesale markets</td></tr>
<tr><td>market_shop_km</td><td>Distance to markets and department stores</td></tr>
<tr><td>fitness_km</td><td>Distance to fitness</td></tr>
<tr><td>swim_pool_km</td><td>Distance to swimming pool</td></tr>
<tr><td>ice_rink_km</td><td>Distance to ice palace</td></tr>
<tr><td>stadium_km</td><td>Distance to stadium</td></tr>
<tr><td>basketball_km</td><td>Distance to the basketball courts</td></tr>
<tr><td>hospice_morgue_km</td><td>Distance to hospice/morgue</td></tr>
<tr><td>detention_facility_km</td><td>Distance to detention facility</td></tr>
<tr><td>public_healthcare_km</td><td>Distance to public healthcare</td></tr>
<tr><td>university_km</td><td>Distance to universities</td></tr>
<tr><td>workplaces_km</td><td>Distance to workplaces</td></tr>
<tr><td>shopping_centers_km</td><td>Distance to shopping centers</td></tr>
<tr><td>office_km</td><td>Distance to business centers/ offices</td></tr>
<tr><td>additional_education_km</td><td>Distance to additional education</td></tr>
<tr><td>preschool_km</td><td>Distance to preschool education organizations</td></tr>
<tr><td>big_church_km</td><td>Distance to large church</td></tr>
<tr><td>church_synagogue_km</td><td>Distance to Christian chirches and Synagogues</td></tr>
<tr><td>mosque_km</td><td>Distance to mosques</td></tr>
<tr><td>theater_km</td><td>Distance to theater</td></tr>
<tr><td>museum_km</td><td>Distance to museums</td></tr>
<tr><td>exhibition_km</td><td>Distance to exhibition</td></tr>
<tr><td>catering_km</td><td>Distance to catering</td></tr>
<tr><td>ecology</td><td>Ecological zone where the house is located</td></tr>
<tr><td>green_part_500</td><td>The share of green zones in 500 meters zone</td></tr>
<tr><td>prom_part_500</td><td>The share of industrial zones in 500 meters zone</td></tr>
<tr><td>office_count_500</td><td>The number of office space in 500 meters zone</td></tr>
<tr><td>office_sqm_500</td><td>The square of office space in 500 meters zone</td></tr>
<tr><td>trc_count_500</td><td>The number of shopping malls in 500 meters zone</td></tr>
<tr><td>trc_sqm_500</td><td>The square of shopping malls in 500 meters zone</td></tr>
<tr><td>cafe_count_500</td><td>The number of cafes or restaurants in 500 meters zone</td></tr>
<tr><td>cafe_sum_500_min_price_avg</td><td>Cafes and restaurant min average bill in 500 meters zone</td></tr>
<tr><td>cafe_sum_500_max_price_avg</td><td>Cafes and restaurant max average bill in 500 meters zone</td></tr>
<tr><td>cafe_avg_price_500</td><td>Cafes and restaurant average bill in 500 meters zone</td></tr>
<tr><td>cafe_count_500_na_price</td><td>Cafes and restaurant bill N/A in 500 meters zone</td></tr>
<tr><td>cafe_count_500_price_500</td><td>Cafes and restaurant bill, average under 500 in 500 meters zone</td></tr>
<tr><td>cafe_count_500_price_1000</td><td>Cafes and restaurant bill, average  500-1000 in 500 meters zone</td></tr>
<tr><td>cafe_count_500_price_1500</td><td>Cafes and restaurant bill, average  1000-1500 in 500 meters zone</td></tr>
<tr><td>cafe_count_500_price_2500</td><td>Cafes and restaurant bill, average  1500-2500 in 500 meters zone</td></tr>
<tr><td>cafe_count_500_price_4000</td><td>Cafes and restaurant bill, average  2500-4000 in 500 meters zone</td></tr>
<tr><td>cafe_count_500_price_high</td><td>Cafes and restaurant bill, average  over 4000 in 500 meters zone</td></tr>
<tr><td>big_church_count_500</td><td>The number of big churchs in 500 meters zone</td></tr>
<tr><td>church_count_500</td><td>The number of churchs in 500 meters zone</td></tr>
<tr><td>mosque_count_500</td><td>The number of mosques in 500 meters zone</td></tr>
<tr><td>leisure_count_500</td><td>The number of leisure facilities in 500 meters zone</td></tr>
<tr><td>sport_count_500</td><td>The number of sport facilities in 500 meters zone</td></tr>
<tr><td>market_count_500</td><td>The number of markets in 500 meters zone</td></tr>
<tr><td>green_part_1000</td><td>The share of green zones in 1000 meters zone</td></tr>
<tr><td>prom_part_1000</td><td>The share of industrial zones in 1000 meters zone</td></tr>
<tr><td>office_count_1000</td><td>The number of office space in 1000 meters zone</td></tr>
<tr><td>office_sqm_1000</td><td>The square of office space in 1000 meters zone</td></tr>
<tr><td>trc_count_1000</td><td>The number of shopping malls in 1000 meters zone</td></tr>
<tr><td>trc_sqm_1000</td><td>The square of shopping malls in 1000 meters zone</td></tr>
<tr><td>cafe_count_1000</td><td>The number of cafes or restaurants in 1000 meters zone</td></tr>
<tr><td>cafe_sum_1000_min_price_avg</td><td>Cafes and restaurant min average bill in 1000 meters zone</td></tr>
<tr><td>cafe_sum_1000_max_price_avg</td><td>Cafes and restaurant max average bill in 1000 meters zone</td></tr>
<tr><td>cafe_avg_price_1000</td><td>Cafes and restaurant average bill in 1000 meters zone</td></tr>
<tr><td>cafe_count_1000_na_price</td><td>Cafes and restaurant bill N/A in 1000 meters zone</td></tr>
<tr><td>cafe_count_1000_price_500</td><td>Cafes and restaurant bill, average under 500 in 1000 meters zone</td></tr>
<tr><td>cafe_count_1000_price_1000</td><td>Cafes and restaurant bill, average  500-1000 in 1000 meters zone</td></tr>
<tr><td>cafe_count_1000_price_1500</td><td>Cafes and restaurant bill, average  1000-1500 in 1000 meters zone</td></tr>
<tr><td>cafe_count_1000_price_2500</td><td>Cafes and restaurant bill, average  1500-2500 in 1000 meters zone</td></tr>
<tr><td>cafe_count_1000_price_4000</td><td>Cafes and restaurant bill, average  2500-4000 in 1000 meters zone</td></tr>
<tr><td>cafe_count_1000_price_high</td><td>Cafes and restaurant bill, average  over 4000 in 1000 meters zone</td></tr>
<tr><td>big_church_count_1000</td><td>The number of big churchs in 1000 meters zone</td></tr>
<tr><td>church_count_1000</td><td>The number of churchs in 1000 meters zone</td></tr>
<tr><td>mosque_count_1000</td><td>The number of mosques in 1000 meters zone</td></tr>
<tr><td>leisure_count_1000</td><td>The number of leisure facilities in 1000 meters zone</td></tr>
<tr><td>sport_count_1000</td><td>The number of sport facilities in 1000 meters zone</td></tr>
<tr><td>market_count_1000</td><td>The number of markets in 1000 meters zone</td></tr>
<tr><td>green_part_1500</td><td>The share of green zones in 1500 meters zone</td></tr>
<tr><td>prom_part_1500</td><td>The share of industrial zones in 1500 meters zone</td></tr>
<tr><td>office_count_1500</td><td>The number of office space in 1500 meters zone</td></tr>
<tr><td>office_sqm_1500</td><td>The square of office space in 1500 meters zone</td></tr>
<tr><td>trc_count_1500</td><td>The number of shopping malls in 1500 meters zone</td></tr>
<tr><td>trc_sqm_1500</td><td>The square of shopping malls in 1500 meters zone</td></tr>
<tr><td>cafe_count_1500</td><td>The number of cafes or restaurants in 1500 meters zone</td></tr>
<tr><td>cafe_sum_1500_min_price_avg</td><td>Cafes and restaurant min average bill in 1500 meters zone</td></tr>
<tr><td>cafe_sum_1500_max_price_avg</td><td>Cafes and restaurant max average bill in 1500 meters zone</td></tr>
<tr><td>cafe_avg_price_1500</td><td>Cafes and restaurant average bill in 1500 meters zone</td></tr>
<tr><td>cafe_count_1500_na_price</td><td>Cafes and restaurant bill N/A in 1500 meters zone</td></tr>
<tr><td>cafe_count_1500_price_500</td><td>Cafes and restaurant bill, average under 500 in 1500 meters zone</td></tr>
<tr><td>cafe_count_1500_price_1000</td><td>Cafes and restaurant bill, average  500-1000 in 1500 meters zone</td></tr>
<tr><td>cafe_count_1500_price_1500</td><td>Cafes and restaurant bill, average  1000-1500 in 1500 meters zone</td></tr>
<tr><td>cafe_count_1500_price_2500</td><td>Cafes and restaurant bill, average  1500-2500 in 1500 meters zone</td></tr>
<tr><td>cafe_count_1500_price_4000</td><td>Cafes and restaurant bill, average  2500-4000 in 1500 meters zone</td></tr>
<tr><td>cafe_count_1500_price_high</td><td>Cafes and restaurant bill, average  over 4000 in 1500 meters zone</td></tr>
<tr><td>big_church_count_1500</td><td>The number of big churchs in 1500 meters zone</td></tr>
<tr><td>church_count_1500</td><td>The number of churchs in 1500 meters zone</td></tr>
<tr><td>mosque_count_1500</td><td>The number of mosques in 1500 meters zone</td></tr>
<tr><td>leisure_count_1500</td><td>The number of leisure facilities in 1500 meters zone</td></tr>
<tr><td>sport_count_1500</td><td>The number of sport facilities in 1500 meters zone</td></tr>
<tr><td>market_count_1500</td><td>The number of markets in 1500 meters zone</td></tr>
<tr><td>green_part_2000</td><td>The share of green zones in 2000 meters zone</td></tr>
<tr><td>prom_part_2000</td><td>The share of industrial zones in 2000 meters zone</td></tr>
<tr><td>office_count_2000</td><td>The number of office space in 2000 meters zone</td></tr>
<tr><td>office_sqm_2000</td><td>The square of office space in 2000 meters zone</td></tr>
<tr><td>trc_count_2000</td><td>The number of shopping malls in 2000 meters zone</td></tr>
<tr><td>trc_sqm_2000</td><td>The square of shopping malls in 2000 meters zone</td></tr>
<tr><td>cafe_count_2000</td><td>The number of cafes or restaurants in 1500 meters zone</td></tr>
<tr><td>cafe_sum_2000_min_price_avg</td><td>Cafes and restaurant min average bill in 2000 meters zone</td></tr>
<tr><td>cafe_sum_2000_max_price_avg</td><td>Cafes and restaurant max average bill in 2000 meters zone</td></tr>
<tr><td>cafe_avg_price_2000</td><td>Cafes and restaurant average bill in 2000 meters zone</td></tr>
<tr><td>cafe_count_2000_na_price</td><td>Cafes and restaurant bill N/A in 2000 meters zone</td></tr>
<tr><td>cafe_count_2000_price_500</td><td>Cafes and restaurant bill, average under 500 in 2000 meters zone</td></tr>
<tr><td>cafe_count_2000_price_1000</td><td>Cafes and restaurant bill, average  500-1000 in 2000 meters zone</td></tr>
<tr><td>cafe_count_2000_price_1500</td><td>Cafes and restaurant bill, average  1000-1500 in 2000 meters zone</td></tr>
<tr><td>cafe_count_2000_price_2500</td><td>Cafes and restaurant bill, average  1500-2500 in 2000 meters zone</td></tr>
<tr><td>cafe_count_2000_price_4000</td><td>Cafes and restaurant bill, average  2500-4000 in 2000 meters zone</td></tr>
<tr><td>cafe_count_2000_price_high</td><td>Cafes and restaurant bill, average  over 4000 in 2000 meters zone</td></tr>
<tr><td>big_church_count_2000</td><td>The number of big churchs in 2000 meters zone</td></tr>
<tr><td>church_count_2000</td><td>The number of churchs in 2000 meters zone</td></tr>
<tr><td>mosque_count_2000</td><td>The number of mosques in 2000 meters zone</td></tr>
<tr><td>leisure_count_2000</td><td>The number of leisure facilities in 2000 meters zone</td></tr>
<tr><td>sport_count_2000</td><td>The number of sport facilities in 2000 meters zone</td></tr>
<tr><td>market_count_2000</td><td>The number of markets in 2000 meters zone</td></tr>
<tr><td>green_part_3000</td><td>The share of green zones in 3000 meters zone</td></tr>
<tr><td>prom_part_3000</td><td>The share of industrial zones in 3000 meters zone</td></tr>
<tr><td>office_count_3000</td><td>The number of office space in 3000 meters zone</td></tr>
<tr><td>office_sqm_3000</td><td>The square of office space in 3000 meters zone</td></tr>
<tr><td>trc_count_3000</td><td>The number of shopping malls in 3000 meters zone</td></tr>
<tr><td>trc_sqm_3000</td><td>The square of shopping malls in 3000 meters zone</td></tr>
<tr><td>cafe_count_3000</td><td>The number of cafes or restaurants in 1500 meters zone</td></tr>
<tr><td>cafe_sum_3000_min_price_avg</td><td>Cafes and restaurant min average bill in 3000 meters zone</td></tr>
<tr><td>cafe_sum_3000_max_price_avg</td><td>Cafes and restaurant max average bill in 3000 meters zone</td></tr>
<tr><td>cafe_avg_price_3000</td><td>Cafes and restaurant average bill in 3000 meters zone</td></tr>
<tr><td>cafe_count_3000_na_price</td><td>Cafes and restaurant bill N/A in 3000 meters zone</td></tr>
<tr><td>cafe_count_3000_price_500</td><td>Cafes and restaurant bill, average under 500 in 3000 meters zone</td></tr>
<tr><td>cafe_count_3000_price_1000</td><td>Cafes and restaurant bill, average  500-1000 in 3000 meters zone</td></tr>
<tr><td>cafe_count_3000_price_1500</td><td>Cafes and restaurant bill, average  1000-1500 in 3000 meters zone</td></tr>
<tr><td>cafe_count_3000_price_2500</td><td>Cafes and restaurant bill, average  1500-2500 in 3000 meters zone</td></tr>
<tr><td>cafe_count_3000_price_4000</td><td>Cafes and restaurant bill, average  2500-4000 in 3000 meters zone</td></tr>
<tr><td>cafe_count_3000_price_high</td><td>Cafes and restaurant bill, average  over 4000 in 3000 meters zone</td></tr>
<tr><td>big_church_count_3000</td><td>The number of big churchs in 3000 meters zone</td></tr>
<tr><td>church_count_3000</td><td>The number of churchs in 3000 meters zone</td></tr>
<tr><td>mosque_count_3000</td><td>The number of mosques in 3000 meters zone</td></tr>
<tr><td>leisure_count_3000</td><td>The number of leisure facilities in 3000 meters zone</td></tr>
<tr><td>sport_count_3000</td><td>The number of sport facilities in 3000 meters zone</td></tr>
<tr><td>market_count_3000</td><td>The number of markets in 3000 meters zone</td></tr>
<tr><td>green_part_5000</td><td>The share of green zones in 5000 meters zone</td></tr>
<tr><td>prom_part_5000</td><td>The share of industrial zones in 5000 meters zone</td></tr>
<tr><td>office_count_5000</td><td>The number of office space in 5000 meters zone</td></tr>
<tr><td>office_sqm_5000</td><td>The square of office space in 5000 meters zone</td></tr>
<tr><td>trc_count_5000</td><td>The number of shopping malls in 5000 meters zone</td></tr>
<tr><td>trc_sqm_5000</td><td>The square of shopping malls in 5000 meters zone</td></tr>
<tr><td>cafe_count_5000</td><td>The number of cafes or restaurants in 1500 meters zone</td></tr>
<tr><td>cafe_sum_5000_min_price_avg</td><td>Cafes and restaurant min average bill in 5000 meters zone</td></tr>
<tr><td>cafe_sum_5000_max_price_avg</td><td>Cafes and restaurant max average bill in 5000 meters zone</td></tr>
<tr><td>cafe_avg_price_5000</td><td>Cafes and restaurant average bill in 5000 meters zone</td></tr>
<tr><td>cafe_count_5000_na_price</td><td>Cafes and restaurant bill N/A in 5000 meters zone</td></tr>
<tr><td>cafe_count_5000_price_500</td><td>Cafes and restaurant bill, average under 500 in 5000 meters zone</td></tr>
<tr><td>cafe_count_5000_price_1000</td><td>Cafes and restaurant bill, average  500-1000 in 5000 meters zone</td></tr>
<tr><td>cafe_count_5000_price_1500</td><td>Cafes and restaurant bill, average  1000-1500 in 5000 meters zone</td></tr>
<tr><td>cafe_count_5000_price_2500</td><td>Cafes and restaurant bill, average  1500-2500 in 5000 meters zone</td></tr>
<tr><td>cafe_count_5000_price_4000</td><td>Cafes and restaurant bill, average  2500-4000 in 5000 meters zone</td></tr>
<tr><td>cafe_count_5000_price_high</td><td>Cafes and restaurant bill, average  over 4000 in 5000 meters zone</td></tr>
<tr><td>big_church_count_5000</td><td>The number of big churchs in 5000 meters zone</td></tr>
<tr><td>church_count_5000</td><td>The number of churchs in 5000 meters zone</td></tr>
<tr><td>mosque_count_5000</td><td>The number of mosques in 5000 meters zone</td></tr>
<tr><td>leisure_count_5000</td><td>The number of leisure facilities in 5000 meters zone</td></tr>
<tr><td>sport_count_5000</td><td>The number of sport facilities in 5000 meters zone</td></tr>
<tr><td>market_count_5000</td><td>The number of markets in 5000 meters zone</td></tr>

</table>
</details>

### A set of macroeconomic indicators, one for each date.(**macro.csv**)
<details>
  <summary>hide/show  **click**</summary>
 
 <table border="1">

   <tr>
    <th>feature</th>
    <th>description</th>

   </tr>
<tr><td> Transaction timestamp</td><td> Transaction timestamp</td></tr>
<tr><td>oil_urals</td><td> Crude Oil Urals (USD/bbl)</td></tr>
<tr><td>gdp_quart</td><td> GDP</td></tr>
<tr><td>gdp_quart_growth</td><td> Real GDP growth</td></tr>
<tr><td>cpi</td><td> Inflation - Consumer Price Index Growth</td></tr>
<tr><td>ppi</td><td> Inflation - Producer Price index Growth</td></tr>
<tr><td>gdp_deflator</td><td> Inflation - GDP deflator</td></tr>
<tr><td>balance_trade</td><td> Trade surplus</td></tr>
<tr><td>balance_trade_growth</td><td> Trade balance (as a percentage of previous year)</td></tr>
<tr><td>usdrub</td><td> Ruble/USD exchange rate</td></tr>
<tr><td>eurrub</td><td> Ruble/EUR exchange rate</td></tr>
<tr><td>brent</td><td> London Brent ($/bbl)</td></tr>
<tr><td>net_capital_export</td><td> Net import / export of capital</td></tr>
<tr><td>gdp_annual</td><td> GDP at current prices</td></tr>
<tr><td>gdp_annual_growth</td><td> GDP growth (in real terms)</td></tr>
<tr><td>average_provision_of_build_contract</td><td> Provision by orders in Russia (for the developer)</td></tr>
<tr><td>average_provision_of_build_contract_moscow</td><td> Provision by orders in Moscow (for the developer)</td></tr>
<tr><td>rts</td><td> Index RTS / return</td></tr>
<tr><td>micex</td><td> MICEX index / return</td></tr>
<tr><td>micex_rgbi_tr</td><td> MICEX index for government bonds (MICEX RGBI TR) / yield</td></tr>
<tr><td>micex_cbi_tr</td><td> MICEX Index corporate bonds (MICEX CBI TR) / yield</td></tr>
<tr><td>deposits_value</td><td> Volume of household deposits</td></tr>
<tr><td>deposits_growth</td><td> Volume growth of population's deposits</td></tr>
<tr><td>deposits_rate</td><td> Average interest rate on deposits</td></tr>
<tr><td>mortgage_value</td><td> Volume of mortgage loans</td></tr>
<tr><td>mortgage_growth</td><td> Growth of mortgage lending</td></tr>
<tr><td>mortgage_rate</td><td> Weighted average rate of mortgage loans</td></tr>
<tr><td>grp</td><td> GRP of the subject of Russian Federation where Apartment is located</td></tr>
<tr><td>grp_growth</td><td> Growth of gross regional product of the subject of the Russian Federation where Apartment is located</td></tr>
<tr><td>income_per_cap</td><td> Average income per capita </td></tr>
<tr><td>real_dispos_income_per_cap_growth</td><td> Growth in real disposable income of Population</td></tr>
<tr><td>salary</td><td> Average monthly salary</td></tr>
<tr><td>salary_growth</td><td> Growth of nominal wages</td></tr>
<tr><td>fixed_basket</td><td> Cost of a fixed basket of consumer goods and services for inter-regional comparisons of purchasing power</td></tr>
<tr><td>retail_trade_turnover</td><td> Retail trade turnover</td></tr>
<tr><td>retail_trade_turnover_per_cap</td><td> Retail trade turnover per capita</td></tr>
<tr><td>retail_trade_turnover_growth</td><td> Retail turnover (in comparable prices in% to corresponding period of previous year)</td></tr>
<tr><td>labor_force</td><td> Size of labor force</td></tr>
<tr><td>unemployment</td><td> Unemployment rate</td></tr>
<tr><td>employment</td><td> Employment rate</td></tr>
<tr><td>invest_fixed_capital_per_cap</td><td> Investments in fixed capital per capita</td></tr>
<tr><td>invest_fixed_assets</td><td> Absolute volume of investments in fixed assets</td></tr>
<tr><td>profitable_enterpr_share</td><td> Share of profitable enterprises</td></tr>
<tr><td>unprofitable_enterpr_share</td><td> The share of unprofitable enterprises</td></tr>
<tr><td>share_own_revenues</td><td> The share of own revenues in the total consolidated budget revenues</td></tr>
<tr><td>overdue_wages_per_cap</td><td> Overdue wages per person</td></tr>
<tr><td>fin_res_per_cap</td><td> The financial results of companies per capita</td></tr>
<tr><td>marriages_per_1000_cap</td><td> Number of marriages per 1,000 people</td></tr>
<tr><td>divorce_rate</td><td> The divorce rate / growth rate</td></tr>
<tr><td>construction_value</td><td> Volume of construction work performed (million rubles)</td></tr>
<tr><td>invest_fixed_assets_phys</td><td> The index of physical volume of investment in fixed assets (in comparable prices in% to the corresponding month of Previous year)</td></tr>
<tr><td>pop_natural_increase</td><td> Rate of natural increase / decrease in Population (1,000 persons)</td></tr>
<tr><td>pop_migration</td><td> Migration increase (decrease) of population</td></tr>
<tr><td>pop_total_inc</td><td> Total population growth</td></tr>
<tr><td>childbirth</td><td> Childbirth</td></tr>
<tr><td>mortality</td><td> Mortality</td></tr>
<tr><td>housing_fund_sqm</td><td> Housing Fund (sqm)</td></tr>
<tr><td>lodging_sqm_per_cap</td><td> Lodging (sqm / pax)</td></tr>
<tr><td>water_pipes_share</td><td> Plumbing availability (pax)</td></tr>
<tr><td>baths_share</td><td> Bath availability (pax)</td></tr>
<tr><td>sewerage_share</td><td> Canalization availability</td></tr>
<tr><td>gas_share</td><td> Gas (mains, liquefied) availability</td></tr>
<tr><td>hot_water_share</td><td> Hot water availability</td></tr>
<tr><td>electric_stove_share</td><td> Electric heating for the floor</td></tr>
<tr><td>heating_share</td><td> Heating availability</td></tr>
<tr><td>old_house_share</td><td> Proportion of old and dilapidated housing, percent</td></tr>
<tr><td>average_life_exp</td><td> Average life expectancy</td></tr>
<tr><td>infant_mortarity_per_1000_cap</td><td> Infant mortality rate (per 1,000 children aged up to one year)</td></tr>
<tr><td>perinatal_mort_per_1000_cap</td><td> Perinatal mortality rate (per 1,000 live births)</td></tr>
<tr><td>incidence_population</td><td> Overall incidence of the total population</td></tr>
<tr><td>rent_price_4+room_bus</td><td> rent price for 4-room apartment, business class</td></tr>
<tr><td>rent_price_3room_bus</td><td> rent price for 3-room apartment, business class</td></tr>
<tr><td>rent_price_2room_bus</td><td> rent price for 2-room apartment, business class</td></tr>
<tr><td>rent_price_1room_bus</td><td> rent price for 1-room apartment, business class</td></tr>
<tr><td>rent_price_3room_eco</td><td> rent price for 3-room apartment, econom class</td></tr>
<tr><td>rent_price_2room_eco</td><td> rent price for 2-room apartment, econom class</td></tr>
<tr><td>rent_price_1room_eco</td><td> rent price for 1-room apartment, econom class</td></tr>
<tr><td>load_of_teachers_preschool_per_teacher</td><td> Load of teachers of preschool educational institutions (number of children per 100 teachers);</td></tr>
<tr><td>child_on_acc_pre_school</td><td> Number of children waiting for the determination to pre-school educational institutions, for capacity of 100</td></tr>
<tr><td>load_of_teachers_school_per_teacher</td><td> Load on teachers in high school (number of pupils in hugh school for 100 teachers)</td></tr>
<tr><td>students_state_oneshift</td><td> Proportion of pupils in high schools with one shift, of the total number of pupils in high schools</td></tr>
<tr><td>modern_education_share</td><td> Share of state (municipal) educational organizations, corresponding to modern requirements of education in the total number of high schools;</td></tr>
<tr><td>old_education_build_share</td><td> The share of state (municipal) educational organizations, buildings are in disrepair and in need of major repairs of the total number.</td></tr>
<tr><td>provision_doctors</td><td> Provision (relative number) of medical doctors in area</td></tr>
<tr><td>provision_nurse</td><td> Provision of nursing staff</td></tr>
<tr><td>load_on_doctors</td><td> The load on doctors (number of visits per physician)</td></tr>
<tr><td>power_clinics</td><td> Capacity of outpatient clinics</td></tr>
<tr><td>hospital_beds_available_per_cap</td><td> Availability of hospital beds per 100 000 persons</td></tr>
<tr><td>hospital_bed_occupancy_per_year</td><td> Average occupancy rate of the hospital beds during a year</td></tr>
<tr><td>provision_retail_space_sqm</td><td> Retail space</td></tr>
<tr><td>provision_retail_space_modern_sqm</td><td> Provision of population with retail space of modern formats, square meter</td></tr>
<tr><td>retail_trade_turnover_per_cap</td><td> Retail trade turnover per capita</td></tr>
<tr><td>turnover_catering_per_cap</td><td> Turnover of catering industry per person</td></tr>
<tr><td>theaters_viewers_per_1000_cap</td><td> Number of theaters viewers per 1000 population</td></tr>
<tr><td>seats_theather_rfmin_per_100000_cap</td><td> Total number of seats in Auditorium of the Ministry of Culture Russian theaters per 100,000 population</td></tr>
<tr><td>museum_visitis_per_100_cap</td><td> Number of visits to museums per 1000 of population</td></tr>
<tr><td>bandwidth_sports</td><td> Capacity of sports facilities</td></tr>
<tr><td>population_reg_sports_share</td><td> Proportion of population regularly doing  sports</td></tr>
<tr><td>students_reg_sports_share</td><td> Proportion of pupils and students regularly doing sports in the total number</td></tr>
<tr><td>apartment_build</td><td> City residential apartment construction</td></tr>
<tr><td>apartment_fund_sqm</td><td> City residential apartment fund</td></tr>


</table>
</details>