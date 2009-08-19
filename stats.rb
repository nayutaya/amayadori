#! ruby -Ku

test_files     = []
tested_files   = []
untested_files = []

Dir.glob("*.py").sort.each { |path|
  if /_test\.py$/i =~ path
    test_files << path
  elsif File.exist?(path.sub(/\.py/i, "_test.py"))
    tested_files << path
  else
    untested_files << path
  end
}

puts "test files:"
test_files.each { |path| puts "  " + path }

puts
puts "tested files:"
tested_files.each { |path| puts "  " + path }

puts
puts "untested_files:"
untested_files.each { |path| puts "  " + path }
