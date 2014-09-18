#!/usr/bin/ruby

require "cgi"
require "tempfile"

oclc_file = Tempfile.new('oclc_nums')
query_file = Tempfile.new('query')

query_file.write("create temporary table OCLC(id text);\n\\copy OCLC from \'#{oclc_file.path}\'\n\\copy (select concat(\'b\',b.record_num,\'a\') as bibno from OCLC o JOIN sierra_view.varfield v ON (o.id = v.field_content and v.varfield_type_code = \'o\') LEFT JOIN sierra_view.bib_view b ON (v.record_id = b.id)) TO STDOUT WITH CSV HEADER;")
query_file.rewind

cgi = CGI.new("html4")
g = cgi["get_oclc"]
if g.length > 0
command = "PGPASSWORD=#{cgi.params["pass"]} /UCUsers/Users/c/crowesn/eresources/pgsq/bin/psql -t -A -U #{cgi.params["username"]} -h sierra-db.libraries.uc.edu -p 1032 -d iii -f #{query_file.path} | mail -s \"OCLC > bibs\" #{cgi.params["email"]}"
oclc_file.write(cgi.params["get_oclc"])
oclc_file.rewind
x = system( command )
end


cgi.out{
	cgi.html{
		cgi.head{ "\n"+cgi.title{"OCLC > Bib no"} } +
		cgi.body{ "\n"+
			cgi.h1 { "OCLC > Bib no " } + "\n"+
			cgi.p{ "Enter credentials below to queue a report of records by OCLC number." } + "\n"+
			cgi.form {"\n"+
			cgi.table {
				cgi.tr {
					cgi.td {"Email"} + cgi.td {cgi.text_field("email")}}+
				cgi.tr {
					cgi.td {"Username"} + cgi.td {cgi.text_field("username")}}+
				cgi.tr {
					cgi.td {"Password"} + cgi.td {cgi.password_field( "pass")}}+
				cgi.tr {
					cgi.td {"OCLC nos"} + cgi.td {cgi.textarea("get_oclc")}}
				}+
			cgi.br +
			cgi.submit +
			#cgi.p{oclc_file.read}+
			cgi.p{x}
			
		}
      }
   }
}
