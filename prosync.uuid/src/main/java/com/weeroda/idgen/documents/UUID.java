package com.weeroda.idgen.documents;

import org.springframework.data.annotation.Id;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;


public class UUID {

    @Id
    private java.util.UUID _id;

    public String getProd_item_uuid() {
        return prod_item_uuid;
    }

    public void setProd_item_uuid(String prod_item_uuid) {
        this.prod_item_uuid = prod_item_uuid;
    }

    private String prod_item_uuid;

    private long exp_duration;
    private long prod_id;

    public int getItemNo() {
        return itemNo;
    }

    public void setItemNo(int itemNo) {
        this.itemNo = itemNo;
    }

    private  int itemNo;

    public long getExp_duration() {
        return exp_duration;
    }

    public void setExp_duration(long exp_duration) {
        this.exp_duration = exp_duration;
    }

    public long getProd_id() {
        return prod_id;
    }

    public void setProd_id(long prod_id) {
        this.prod_id = prod_id;
    }

    public long getOrg_id() {
        return org_id;
    }

    public void setOrg_id(long org_id) {
        this.org_id = org_id;
    }

    public String getAdded_date() {
        return added_date;
    }

    public void setAdded_date(String added_date) {
        this.added_date = added_date;
    }

    private long org_id;
    private String added_date;



    public UUID(long exp_duration, long prod_id, long org_id,String added_date, int itemNo) {
        
        this._id = java.util.UUID.randomUUID();
        try {
            this.prod_item_uuid = toHexString(getSHA(prod_id + ":" + org_id + ":" + exp_duration + ":" + added_date + ":" + itemNo));
        }catch(NoSuchAlgorithmException ex){
            this.prod_item_uuid="000000";
        }
        this.exp_duration = exp_duration;
        this.prod_id = prod_id;
        this.org_id = org_id;
        this.added_date = added_date;
        this.itemNo = itemNo;
    }

    public java.util.UUID get_id() {
        return _id;
    }

    private static byte[] getSHA(String input) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        return md.digest(input.getBytes(StandardCharsets.UTF_8));
    }

    private static String toHexString(byte[] hash) {
        BigInteger number = new BigInteger(1, hash);
        StringBuilder hexString = new StringBuilder(number.toString(16));
        while (hexString.length() < 32) {
            hexString.insert(0, '0');
        }
        return hexString.toString();
    }


}
