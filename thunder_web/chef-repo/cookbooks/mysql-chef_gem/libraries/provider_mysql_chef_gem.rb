class Chef
  class Provider
    class MysqlChefGem < Chef::Provider::LWRPBase
      use_inline_resources if defined?(use_inline_resources)

      def whyrun_supported?
        true
      end

      def action_install
        converge_by 'install mysql chef_gem and dependencies' do
          recipe_eval do
            run_context.include_recipe 'build-essential::default'
          end

          recipe_eval do
            run_context.include_recipe 'mysql::client'
          end          
          
          # changed to instll from source file - to prevent external net connection 
          gem_file_name = "mysql-2.9.1.gem"
          chef_gem 'mysql' do
            action :install
            source "#{node['thunder']['thunder_package_dir']}/#{gem_file_name}"
            version "2.9.1"
          end
          
        end
      end

      def action_remove
        chef_gem 'mysql' do
          action :remove
        end
      end
    end
  end
end
