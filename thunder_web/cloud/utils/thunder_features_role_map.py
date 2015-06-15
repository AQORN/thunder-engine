# Add roles and feature mapping here
# @author: Deepthy
# @create_date: 01-Apr-2015
# @modified by: Deepthy   
# @modified_date: 01-Apr-2015
# @description: RBAC feature accesses of the users

# Privilge - feature access list for the roles
roleFeatureMapping = {}
roleFeatureMapping['ThunderAdmin'] = ["add_cloud", "del_cloud", "deploy_cloud", "edit_config", "reschedule_job", "view_config", "feature_control", "addon_control"]
roleFeatureMapping['CloudAdmin'] = ["deploy_cloud", "edit_config", "reschedule_job", "view_config"]
roleFeatureMapping['Engineer'] = ["edit_config", "view_config"]
roleFeatureMapping['User'] = ["view_config"]
