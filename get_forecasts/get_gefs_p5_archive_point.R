library(tidyverse)
library(sf)
library(aws.s3)
library(feather)

get_gefs_p5_archive_point <- function(date, model, horizon, lat, lon, loc_id) {
  tryCatch(
    {
      # get forecast
      save_object(
        object = paste0("gefs.", date, "/06/atmos/pgrb2ap5/", model, ".t06z.pgrb2a.0p50.f", horizon),
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
      
      names(loc_extr)[c(60:68, 78, 79)] <- c("WEASD", "SNOD", "ICETK", "TMP", "RH", 
                                             "TMAX", "TMIN", "UGRD", "VGRD", "DSWRF", 
                                             "DLWRF")
      
      loc_extr %>% 
        select("WEASD", "SNOD", "ICETK", "TMP", "RH", "TMAX", "TMIN", 
               "UGRD", "VGRD", "DSWRF", "DLWRF") %>% 
        mutate(loc = loc_id, 
               date = date, 
               model = model, 
               horizon = horizon, 
               gefs = "gefs_0p5")
    },
    error = function(e) {
      message(paste0("Could not gather forecasts for model ", model, 
                     " at timestep ", horizon,
                     " on ", date))
      return(NULL)
    }
  )
}



# variable lists ----------------------------------------------------------

models <- c("gec00", "gep01", "gep02", "gep03", "gep04", "gep05", "gep06",
            "gep07", "gep08", "gep09", "gep10", "gep11", "gep12", "gep13", 
            "gep14", "gep15", "gep16", "gep17", "gep18", "gep19", "gep20",
            "gep21", "gep22", "gep23", "gep24", "gep25", "gep26", "gep27",
            "gep28", "gep29", "gep30")

horizons <- c("012", "036", "060", "084", "108", "132", "156", "180", "204", "228")

lon <- 105.85
lat <- 40.22

loc_id <- "SMR"


# 2022 --------------------------------------------------------------------

date_list_2022 <- format(
  seq.Date(ymd("2022-05-01"), ymd("2022-11-01"), by = "1 day"),
  "%Y%m%d")

for (d in date_list_2022) {
  message(paste0("Retrieving forecasts for ", d))
  all_iterations <- expand.grid(d, models, horizons, lon, lat, loc_id) 
  colnames(all_iterations) <- c("date", "model", "horizon", "lon", "lat", "loc_id")
  gefs_extr <- pmap(.l = list(all_iterations$date,
                              all_iterations$model,
                              all_iterations$horizon,
                              all_iterations$lon,
                              all_iterations$lat,
                              all_iterations$loc_id),
                    .f = get_gefs_p5_archive_point) %>% 
    bind_rows()
  write_feather(gefs_extr, paste0("data/forecasts/gefs_p5_", d, ".feather"))
}

# 2023 --------------------------------------------------------------------

date_list_2023 <- format(
  seq.Date(ymd("2023-05-01"), ymd("2023-11-01"), by = "1 day"),
  "%Y%m%d")

for (d in date_list_2023) {
  all_iterations <- expand.grid(d, models, horizons, lon, lat, loc_id) 
  colnames(all_iterations) <- c("date", "model", "horizon", "lon", "lat", "loc_id")
  gefs_extr <- pmap(.l = list(all_iterations$date,
                              all_iterations$model,
                              all_iterations$horizon,
                              all_iterations$lon,
                              all_iterations$lat,
                              all_iterations$loc_id),
                    .f = get_gefs_p5_archive_point) %>% 
    bind_rows()
  write_feather(gefs_extr, paste0("data/forecasts/gefs_p5_", date, ".feather"))
}
