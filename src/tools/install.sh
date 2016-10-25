# Special.
rm -f ~/bin/run_nolock
ln -s `pwd`/run_nolock.py ~/bin/run_nolock

rm -f ~/bin/get_job_machine
bazel run --script_path ~/bin/get_job_machine :get_job_machine

rm -f ~/bin/kill_all_jobs
bazel run --script_path ~/bin/kill_all_jobs :kill_all_jobs

rm -f ~/bin/show_all_jobs
bazel run --script_path ~/bin/show_all_jobs :show_all_jobs

rm -f ~/bin/follow_log
bazel run --script_path ~/bin/follow_log :follow_log
