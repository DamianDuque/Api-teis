def getstates():
    return str("""SELECT cf."state", pd."PD_id"
FROM public."CensusForm" cf
JOIN public."CensusRespondent" cr ON cf."ECN" = cr."CensusForm_ECN"
JOIN public."PrivateDwelling" pd ON cr."PrivateDwelling_PD_id" = pd."PD_id"
JOIN public."CensusCollector" cc ON pd."CensusCollector_CWL" = cc."CWL"
WHERE cc."CWL" = %s;""")

def update_CFN():
    return str("""UPDATE public."PrivateDwelling"
                     SET "CFN" = %s
                     WHERE "PD_id" = %s;""")

def update_state():
    return str("""UPDATE public."CensusForm"
SET "state" = %s
FROM public."CensusRespondent" cr
JOIN public."PrivateDwelling" pd ON cr."PrivateDwelling_PD_id" = %s
WHERE cr."CensusForm_ECN" = public."CensusForm"."ECN"
  AND pd."PD_id" = '1';""")