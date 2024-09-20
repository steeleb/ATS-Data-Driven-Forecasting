library(tidyverse)
library(sf)
library(aws.s3)
library(feather)

get_gefs_p25_archive_point <- function(date, model, horizon, lat, lon, loc_id) {
  # get forecast
  save_object(
    object = paste0("gefs.", date, "/06/atmos/pgrb2sp25/", model, ".t06z.pgrb2a.0p25.f", horizon),
    bucket = "s3://noaa-gefs-pds/",
    region = "us-east-1",
    file = "temp.grb2"
  )
  
  # load forecast
  gefs <- read_stars("temp.grb2")
  
  # extract for location
  loc_sf <- st_point(c(lon, lat)) %>% 
    st_sfc(., crs = "EPSG:4326")
  
  loc_extr <- st_extract(gefs, st_transform(loc_sf, crs = st_crs(gefs))) %>% 
    st_as_sf() %>% 
    st_drop_geometry() 
  
  names(loc_extr)[c(1, 5, 8, 11:16, 19, 26, 27)] <- c("GUST", "WEASD", "TMP", "TMAX", "TMIN", 
                                                      "UGRD", "VGRD", "APCP", "CSNOW", "CRAIN", 
                                                      "DSWRF", "DLWRF")

  loc_extr %>% 
    select("GUST", "WEASD", "TMP", "TMAX", "TMIN", 
           "UGRD", "VGRD", "APCP", "CSNOW", "CRAIN", 
           "DSWRF", "DLWRF") %>% 
    mutate(loc = loc_id, 
           date = date, 
           model = model, 
           horizon = horizon, 
           gefs = "gefs_0p25")
}


# variable lists ----------------------------------------------------------

models <- c("gec00", "gep01", "gep02", "gep03", "gep04", "gep05", "gep06",
            "gep07", "gep08", "gep09", "gep10", "gep11", "gep12", "gep13", 
            "gep14", "gep15", "gep16", "gep17", "gep18", "gep19", "gep20",
            "gep21", "gep22", "gep23", "gep24", "gep25", "gep26", "gep27",
            "gep28", "gep29", "gep30")

horizons <- c("012", "036", "060", "084", "108", "132", "156", "190", "214")

lon <- 105.85
lat <- 40.22

loc_id <- "SMR"


# 2021 --------------------------------------------------------------------

date_list_2021 <- format(
  seq.Date(ymd("2021-05-01"), ymd("2021-11-01"), by = "1 day"),
  "%Y%m%d")

all_data_2021 <- expand.grid(date_list_2021, models, horizons, lon, lat, loc_id) 
colnames(all_data_2021) <- c("date", "model", "horizon", "lon", "lat", "loc_id")

gefs_2021 <- pmap(.l = list(all_data_2021$date,
                            all_data_2021$model,
                            all_data_2021$horizon,
                            all_data_2021$lon,
                            all_data_2021$lat,
                            all_data_2021$loc_id),
                  .f = get_gefs_p25_archive_point) %>% 
  bind_rows()

write_feather(gefs_2021, "data/forecasts/gefs_p25_2021.feather")


# 2022 --------------------------------------------------------------------

date_list_2022 <- format(
  seq.Date(ymd("2022-05-01"), ymd("2022-11-01"), by = "1 day"),
  "%Y%m%d")

all_data_2022 <- expand.grid(date_list_2022, models, horizons, lon, lat, loc_id) 
colnames(all_data_2022) <- c("date", "model", "horizon", "lon", "lat", "loc_id")

gefs_2022 <- pmap(.l = list(all_data_2022$date,
                            all_data_2022$model,
                            all_data_2022$horizon,
                            all_data_2022$lon,
                            all_data_2022$lat,
                            all_data_2022$loc_id),
                  .f = get_gefs_p25_archive_point) %>% 
  bind_rows()

write_feather(gefs_2022, "data/forecasts/gefs_p25_2022.feather")


# 2023 --------------------------------------------------------------------

date_list_2023 <- format(
  seq.Date(ymd("2023-05-01"), ymd("2023-11-01"), by = "1 day"),
  "%Y%m%d")

all_data_2023 <- expand.grid(date_list_2023, models, horizons, lon, lat, loc_id) 
colnames(all_data_2023) <- c("date", "model", "horizon", "lon", "lat", "loc_id")

gefs_2023 <- pmap(.l = list(all_data_2023$date,
                            all_data_2023$model,
                            all_data_2023$horizon,
                            all_data_2023$lon,
                            all_data_2023$lat,
                            all_data_2023$loc_id),
                  .f = get_gefs_p25_archive_point) %>% 
  bind_rows()

write_feather(gefs_2023, "data/forecasts/gefs_p25_2023.feather")

