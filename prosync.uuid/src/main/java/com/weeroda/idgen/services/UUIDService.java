package com.weeroda.idgen.services;

import com.weeroda.idgen.documents.UUID;
import com.weeroda.idgen.dto.UUIDCreateDTO;
import com.weeroda.idgen.dto.UUIDUpdateDTO;

import java.util.List;

public interface UUIDService {

    public List<UUID> getAllUUID(long orgId);
    public List<UUID> getAllUUID(long orgId,long prodID);
    public UUID getUUIDById(String id);
    public boolean createUUID(List<UUID> uuids);
    public List<UUID> generateUUID(UUIDCreateDTO UUIDCreateDTO);
    public UUID updateUUID(UUIDUpdateDTO UUIDUpdateDTO, java.util.UUID id);
    public UUID deleteUUIDById(java.util.UUID id);
}
