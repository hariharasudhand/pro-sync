package com.weeroda.idgen.dto;



public class UUIDCreateDTO {

    private long exp_duration;

    public long getExp_duration() {
        return exp_duration;
    }

    public void setExp_duration(long exp_duration) {
        this.exp_duration = exp_duration;
    }

    private long prod_id;

    public long getProd_id() {
        return prod_id;
    }

    public void setProd_id(long prod_id) {
        this.prod_id = prod_id;
    }


    private long org_id;

    public long getOrg_id() {
        return org_id;
    }

    public void setOrg_id(long org_id) {
        this.org_id = org_id;
    }


    private String added_date;

    public String getAdded_date() {
        return added_date;
    }

    public void setAdded_date(String added_date) {
        this.added_date = added_date;
    }


    public int getTotal_ids() {
        return total_ids;
    }

    public void setTotal_ids(int total_ids) {
        this.total_ids = total_ids;
    }

    private int total_ids;


}
